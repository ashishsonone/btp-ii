# python run.py 2 lxc apache data0

#parameters 
#1 n  - number of vms/containers
#2 lxc/kvm
#3 apache/mysql
#4 foldername - where experiment output will be stored

import sys
import os
import time
from subprocess import call

run_number = 0

def create_lxc_containers(n, load):
    for i in range(int(n)):
        container_name = "temp-" + load + "-" + str(i)
        print(container_name)
        call(["lxc-clone",  "-o",  load + "-master",  "-n", container_name ])
    print(str(n) + "containers for " + load + " created")

def destroy_lxc_containers(n, load):
    for i in range(int(n)):
        container_name = "temp-" + load + "-" + str(i)
        print(container_name)
        call(["lxc-stop",  "-n", container_name])
        call(["lxc-destroy",  "-n", container_name])
    print(str(n) + "containers for " + load + " destroyed")

def run_lxc(n, load):
    call(["lxc-ls"])
    for i in range(n):
        container_name = "temp-" + load + "-" + str(i)
        call(["lxc-start",  "-n", container_name, "-d"])
    time.sleep(3)
    call(["lxc-ls"])
    #clean up

def stop_lxc(n, load):
    for i in range(n):
        container_name = "temp-" + load + "-" + str(i)
        command = "lxc-stop" +  " -n " +  container_name 
        print(command)
        call(["lxc-stop",  "-n", container_name])
    call(["lxc-ls"])

def run_kvm(final_mac, vnc, telnet, name, disk):
    print("spawning " + disk + "mac = " + final_mac + " vnc = " + str(vnc) + " telnet = " + str(telnet))
    os.system("qemu-system-x86_64 -name " + name + " -m 256 -enable-kvm -smp 1 -drive file=/mnt/local/" + disk + ",if=none,id=drive-virtio-disk0,format=qcow2,cache=none -device virtio-blk-pci,drive=drive-virtio-disk0,id=virtio-disk0 -netdev tap,id=hostnet0,script=/etc/qemu-ifup,downscript=/etc/qemu-ifdown -device virtio-net-pci,netdev=hostnet0,id=net0,mac="+ final_mac + " -device virtio-balloon-pci,id=balloon0 -boot c -vga cirrus -monitor telnet:10.129.34.2:" + str(telnet) + ",server,nowait " + "--daemonize -vnc 10.129.34.2:" + str(vnc))

def stop_kvm(telnet):
    print("Stopping kvm with telnet port " + str(telnet))
    os.system("./stop.sh " + str(telnet))

def start_all_kvm(n, load, folder):
    print("stopping uksm")
    os.system("echo 0 > /sys/kernel/mm/uksm/run")
    os.system("cat /sys/kernel/mm/uksm/run")

    folder_idle = folder + "/idle"
    folder_without_uksm = folder + "/without"
    folder_with_uksm = folder + "/with"

    print("creating folders " + folder)
    call(["mkdir", "-p" , folder])
    call(["mkdir", "-p" , folder_idle])
    call(["mkdir", "-p" , folder_without_uksm])
    call(["mkdir", "-p" , folder_with_uksm])


    idle_duration = 5
    os.system("top -b -d 1 -n " + str(idle_duration) + " > " +  folder_idle + "/top &")
    os.system("python data_collect.py " + str(idle_duration) + " " + folder_idle + " &")

    print("sleeping for " + str(int(idle_duration*1.2)))
    time.sleep(int(idle_duration*1.2))
    
    print("Starting KVMs...")
    if(load == "mysql"):
        base_mac = "42:54:00:cf:eb:"
        base_vnc = 6600
        base_telnet = 6500
    elif(load == "apache"):
        base_mac = "40:54:00:cf:ec:"
        base_vnc = 5400
        base_telnet = 5500
    else:
        print("Incorrect load name. Returning")
    
    boot_duration = 60 * 3
    mac = 0
    for i in range(5, 5+n):
        mac_str = "%02d" % (mac+i,)
        final_mac = base_mac + mac_str
        print("mac is " + final_mac)
        name = "t" + str(i)
        disk = "temp-" + load + "-" + str(i) + ".qcow"
        vnc = base_vnc + i
        telnet = base_telnet + i
        run_kvm(final_mac, vnc, telnet, name, disk)
    os.system("ps -e | grep qemu-system")
    print("sleeping for " + str(int(boot_duration*1.1)))
    time.sleep(int(boot_duration*1.1))
  
    without_duration = 60 * 5
    os.system("top -b -d 1 -n " + str(without_duration) + " > " +  folder_without_uksm + "/top &")
    os.system("python data_collect.py " + str(without_duration) + " " + folder_without_uksm + " &")
    
    #Start oltp benchmark
    os.system("ssh root@10.129.34.7 'sh /root/Desktop/load.sh kvm " + str(run_number) + "' &")
    
    print("sleeping for " + str(int(without_duration*1.1)))
    time.sleep(int(without_duration*1.1))
    os.system("ssh root@10.129.34.7 'killall oltpbenchmark' &")
    
    print("starting uksm")
    os.system("echo 1 > /sys/kernel/mm/uksm/run")
    os.system("cat /sys/kernel/mm/uksm/run")

    #Start oltp benchmark
    os.system("ssh root@10.129.34.7 'sh /root/Desktop/load.sh kvm " + str(run_number) + "' &")
    
    with_duration = 60 * 5
    os.system("top -b -d 1 -n " + str(with_duration) + " > " +  folder_with_uksm + "/top &")
    os.system("python data_collect.py " + str(with_duration) + " " + folder_with_uksm)
    print("data collected. Now stopping the kvms")
    
    os.system("ssh root@10.129.34.7 'killall oltpbenchmark' &")
    for i in range(n):
        telnet = base_telnet + i
        stop_kvm(telnet)
        
    print("DONE")
    os.system("ps -e | grep qemu-system")
    
    #"""

def experiment_lxc(n, load, folder):
    print("stopping uksm")
    os.system("echo 0 > /sys/kernel/mm/uksm/run")
    os.system("cat /sys/kernel/mm/uksm/run")

    folder_idle = folder + "/idle"
    folder_without_uksm = folder + "/without"
    folder_with_uksm = folder + "/with"

    print("creating folders " + folder)
    call(["mkdir", "-p" , folder])
    call(["mkdir", "-p" , folder_idle])
    call(["mkdir", "-p" , folder_without_uksm])
    call(["mkdir", "-p" , folder_with_uksm])


    idle_duration = 5
    os.system("top -b -d 1 -n " + str(idle_duration) + " > " +  folder_idle + "/top &")
    os.system("python data_collect.py " + str(idle_duration) + " " + folder_idle + " &")

    print("sleeping for " + str(int(idle_duration*1.2)))
    time.sleep(int(idle_duration*1.2))

    print("running " + str(n) +  "lxc containers for " + load)
    run_lxc(n, load)

    boot_duration = 60 * 3
    print("sleeping for " + str(int(boot_duration*1.1)))
    time.sleep(int(boot_duration*1.1))
    
    without_duration = 60 * 5
    os.system("top -b -d 1 -n " + str(without_duration) + " > " +  folder_without_uksm + "/top &")
    os.system("python data_collect.py " + str(without_duration) + " " + folder_without_uksm + " &")

    #Start oltp benchmark
    os.system("ssh root@10.129.34.7 'sh /root/Desktop/load.sh lxc " + str(run_number) + "' &")
    print("sleeping for " + str(int(without_duration*1.1)))
    time.sleep(int(without_duration*1.1))
    os.system("ssh root@10.129.34.7 'killall oltpbenchmark' &")

    print("starting uksm")
    os.system("echo 1 > /sys/kernel/mm/uksm/run")
    os.system("cat /sys/kernel/mm/uksm/run")

    #Start oltp benchmark
    os.system("ssh root@10.129.34.7 'sh /root/Desktop/load.sh lxc " + str(run_number) + "' &")
    
    with_duration = 60 * 5
    os.system("top -b -d 1 -n " + str(with_duration) + " > " +  folder_with_uksm + "/top &")
    os.system("python data_collect.py " + str(with_duration) + " " + folder_with_uksm)
    print("data collected. Now stopping the containers")
    os.system("ssh root@10.129.34.7 'killall oltpbenchmark' &")
    stop_lxc(n, load)
    call(["lxc-ls"])
    print("DONE")



for i in range(3):
    run_number = i
    data_folder = "DATA_LOAD/exp" + str(i) + "-kvm-mysql"
    os.system("sudo sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches'")
    start_all_kvm(5, "mysql", data_folder)
print("KVM MySql DONE! >>>>>>>>>>>>>>>>>>>>>>>>")
for i in range(3):
    run_number = i
    data_folder = "DATA_LOAD/exp" + str(i) + "-lxc-mysql"
    os.system("sudo sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches'")
    experiment_lxc(5, "mysql", data_folder)
print("LXC mysql DONE! >>>>>>>>>>>>>>>>>>>>>>>>")
