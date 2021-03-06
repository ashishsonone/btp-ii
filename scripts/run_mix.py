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

def start_all_kvm_mix(n, folder):
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
    base_mac_mysql = "42:54:00:cf:eb:"
    base_vnc_mysql = 6600
    base_telnet_mysql = 6500
    base_mac_apache = "40:54:00:cf:ec:"
    base_vnc_apache = 5400
    base_telnet_apache = 5500
    
    """
    """
    without_duration = 60 * 3
    os.system("top -b -d 1 -n " + str(without_duration) + " > " +  folder_without_uksm + "/top &")
    os.system("python data_collect.py " + str(without_duration) + " " + folder_without_uksm + " &")


    mac = 0
    for i in range(n/2+1):
        mac_str = "%02d" % (mac+i,)
        final_mac = base_mac_mysql + mac_str
        print("mac is " + final_mac)
        name = "t" + str(i)
        disk = "temp-mysql" + "-" + str(i) + ".qcow"
        vnc = base_vnc_mysql + i
        telnet = base_telnet_mysql + i
        run_kvm(final_mac, vnc, telnet, name, disk)
        
    for i in range(n/2):
        mac_str = "%02d" % (mac+i,)
        final_mac = base_mac_apache + mac_str
        print("mac is " + final_mac)
        name = "t" + str(i)
        disk = "temp-apache" + "-" + str(i) + ".qcow"
        vnc = base_vnc_apache + i
        telnet = base_telnet_apache + i
        run_kvm(final_mac, vnc, telnet, name, disk)

    os.system("ps -e | grep qemu-system")
    print("sleeping for " + str(int(without_duration*1.1)))
    time.sleep(int(without_duration*1.1))

    
    """
    """
    print("starting uksm")
    os.system("echo 1 > /sys/kernel/mm/uksm/run")
    os.system("cat /sys/kernel/mm/uksm/run")

    with_duration = 60 * 7
    os.system("top -b -d 1 -n " + str(with_duration) + " > " +  folder_with_uksm + "/top &")
    os.system("python data_collect.py " + str(with_duration) + " " + folder_with_uksm)
    print("data collected. Now stopping the kvms")
    """
    #"""
    
    for i in range(n/2+1):
        telnet = base_telnet_mysql + i
        stop_kvm(telnet)
        
    for i in range(n/2):
        telnet = base_telnet_apache + i
        stop_kvm(telnet)

    print("DONE")
    os.system("ps -e | grep qemu-system")
    """
    #"""

def experiment_lxc_mix(n, folder):
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

    without_duration = 60 * 3
    os.system("top -b -d 1 -n " + str(without_duration) + " > " +  folder_without_uksm + "/top &")
    os.system("python data_collect.py " + str(without_duration) + " " + folder_without_uksm + " &")

    #print("running " + str(n) +  "lxc containers for " + load)
    run_lxc(n/2+1, "mysql")
    run_lxc(n/2, "apache")

    print("sleeping for " + str(int(without_duration*1.1)))
    time.sleep(int(without_duration*1.1))

    print("starting uksm")
    os.system("echo 1 > /sys/kernel/mm/uksm/run")
    os.system("cat /sys/kernel/mm/uksm/run")

    with_duration = 60 * 7
    os.system("top -b -d 1 -n " + str(with_duration) + " > " +  folder_with_uksm + "/top &")
    os.system("python data_collect.py " + str(with_duration) + " " + folder_with_uksm)
    print("data collected. Now stopping the containers")
    stop_lxc(n/2+1, "mysql")
    stop_lxc(n/2, "apache")
    call(["lxc-ls"])
    print("DONE")

""" 
if(sys.argv[2]=="lxc"):
    experiment_lxc(sys.argv[1], sys.argv[3], sys.argv[4])
""" 
'''
for i in range(3):
    print("Exp No " + str(i))
    os.system("sudo sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches'")
    start_all_kvm(10, "apache", "long-" + str(i) + "-kvm-apache-10")
'''

for i in range(3):
    data_folder = "DATA1/exp" + str(i) + "-kvm-mix"
    os.system("sudo sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches'")
    start_all_kvm_mix(5, data_folder)

print("KVM mix DONE! >>>>>>>>>>>>>>>>>>>>>>>>")

for i in range(3):
    data_folder = "DATA1/exp" + str(i) + "-lxc-mix"
    os.system("sudo sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches'")
    experiment_lxc_mix(5, data_folder)

print("lxc mix DONE! >>>>>>>>>>>>>>>>>>>>>>>>")

#start_all_kvm(10, "mysql", "temp")
#experiment_lxc(2, "apache", "temp-3")

"""
for i in range(3):
    print("Exp No " + str(i))
    os.system("sudo sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches'")
    experiment_lxc("10", "apache", "long-" + str(i) + "-lxc-apache-10")
"""

#stop_lxc("10", "mysql")
#stop_lxc("10", "apache")
#experiment_lxc("10", "mysql", "data-lxc-mysql-10")
#create_kvm_qcow_images(15, "apache")
#create_kvm_qcow_images(15, "apache")

#create_lxc_containers(15, "apache")
#create_lxc_containers(15, "mysql")
#destroy_lxc_containers(15, "apache")
#destroy_lxc_containers(15, "mysql")
