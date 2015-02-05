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
    for i in range(int(n)):
        container_name = "temp-" + load + "-" + str(i)
        call(["lxc-start",  "-n", container_name, "-d"])
    time.sleep(3)
    call(["lxc-ls"])
    #clean up

def stop_lxc(n, load):
    for i in range(int(n)):
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

    folder_without_uksm = folder + "/without"
    folder_with_uksm = folder + "/with"

    print("creating folders " + folder)
    call(["mkdir", "-p" , folder])
    call(["mkdir", "-p" , folder_without_uksm])
    call(["mkdir", "-p" , folder_with_uksm])


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
    
    mac = 0
    
    for i in range(n):
        mac_str = "%02d" % (mac+i,)
        final_mac = base_mac + mac_str
        print("mac is " + final_mac)
        name = "t" + str(i)
        disk = "temp-" + load + "-" + str(i) + ".qcow"
        vnc = base_vnc + i
        telnet = base_telnet + i
        run_kvm(final_mac, vnc, telnet, name, disk)
        
    os.system("ps -e | grep qemu-system")
    
    #experiment here
    print("Experiment is on")
    time.sleep(300) #wait for 5 minutes for system to stabalize
    
    print("now collecting data without uksm")
    #without uksm experiment for 60 second
    without_duration = 60
    os.system("top -b -d 1 -n " + str(without_duration) + " > " +  folder_without_uksm + "/top &")
    for i in range(without_duration):
        data_folder = folder_without_uksm + "/" + str(i);
        call(["mkdir", data_folder])
        os.system("free -m > " + data_folder + "/" + "free")
        os.system("cp /sys/kernel/mm/uksm/pages_* " + data_folder)
        time.sleep(1)


    print("starting uksm")
    os.system("echo 1 > /sys/kernel/mm/uksm/run")
    os.system("cat /sys/kernel/mm/uksm/run")

    with_duration = 60 * 10
    os.system("top -b -d 1 -n " + str(with_duration) + " > " +  folder_with_uksm + "/top &")
    for i in range(with_duration):
        data_folder = folder_with_uksm + "/" + str(i);
        call(["mkdir", data_folder])
        os.system("free -m > " + data_folder + "/" + "free")
        os.system("cp /sys/kernel/mm/uksm/pages_* " + data_folder)
        time.sleep(1)
    print("data collected. Now stopping the kvms")
    
    for i in range(n):
        telnet = base_telnet + i
        stop_kvm(telnet)
        
    print("done")
    os.system("ps -e | grep qemu-system")

def experiment_lxc(n, load, folder):
    print("stopping uksm")
    os.system("echo 0 > /sys/kernel/mm/uksm/run")
    os.system("cat /sys/kernel/mm/uksm/run")

    folder_without_uksm = folder + "/without"
    folder_with_uksm = folder + "/with"

    print("creating folders " + folder)
    call(["mkdir", "-p" , folder])
    call(["mkdir", "-p" , folder_without_uksm])
    call(["mkdir", "-p" , folder_with_uksm])

    print("running lxc containers for " + load)
    run_lxc(n, load)

    time.sleep(300)

    call(["lxc-ls"])
    print("now collecting data without uksm")
    #without uksm experiment for 60 seconds
    without_duration = 60
    os.system("top -b -d 1 -n " + str(without_duration) + " > " +  folder_without_uksm + "/top &")
    for i in range(without_duration):
        data_folder = folder_without_uksm + "/" + str(i);
        call(["mkdir", data_folder])
        os.system("free -m > " + data_folder + "/" + "free")
        os.system("cp /sys/kernel/mm/uksm/pages_* " + data_folder)
        time.sleep(1)


    print("starting uksm")
    os.system("echo 1 > /sys/kernel/mm/uksm/run")
    os.system("cat /sys/kernel/mm/uksm/run")

    with_duration = 60 * 10
    os.system("top -b -d 1 -n " + str(with_duration) + " > " +  folder_with_uksm + "/top &")
    for i in range(with_duration):
        data_folder = folder_with_uksm + "/" + str(i);
        call(["mkdir", data_folder])
        os.system("free -m > " + data_folder + "/" + "free")
        os.system("cp /sys/kernel/mm/uksm/pages_* " + data_folder)
        time.sleep(1)
    print("data collected. Now stopping the containers")
    stop_lxc(n, load)
    call(["lxc-ls"])
    print("DONE")

""" 
if(sys.argv[2]=="lxc"):
    experiment_lxc(sys.argv[1], sys.argv[3], sys.argv[4])
""" 
"""
for i in range(3):
    print("Exp No " + str(i))
    os.system("sudo sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches'")
    start_all_kvm(10, "apache", "long-" + str(i) + "-kvm-apache-10")
"""

for i in range(3):
    print("Exp No " + str(i))
    os.system("sudo sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches'")
    experiment_lxc("10", "apache", "long-" + str(i) + "-lxc-apache-10")

#experiment_lxc("10", "mysql", "data-lxc-mysql-10")
#create_kvm_qcow_images(15, "apache")
#create_kvm_qcow_images(15, "apache")

#create_lxc_containers(15, "apache")
#create_lxc_containers(15, "mysql")
#destroy_lxc_containers(15, "apache")
#destroy_lxc_containers(15, "mysql")
