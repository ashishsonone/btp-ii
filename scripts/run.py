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

def create_kvm_qcow_images(n, load):
    for i in range(int(n)):
        base = "/mnt/local/"
        image_name = "temp-" + load + "-" + str(i) + ".qcow"
        print(image_name)
        call(["qemu-img",  "create", "-f", "qcow2", "-b", base + load + "UbuntuServerHardDisk.img", base + image_name])
    print(str(n) + "containers for " + load + " created")

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

    time.sleep(60);

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

    with_duration = 60 * 5
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

""" """
if(sys.argv[2]=="lxc"):
    experiment_lxc(sys.argv[1], sys.argv[3], sys.argv[4])
""" """
#create_kvm_qcow_images(15, "apache")
#create_kvm_qcow_images(15, "mysql")

#create_lxc_containers(15, "apache")
#create_lxc_containers(15, "mysql")
#destroy_lxc_containers(15, "apache")
#destroy_lxc_containers(15, "mysql")
