import sys
import os
import time
from subprocess import call

duration = int(sys.argv[1])
base_folder = sys.argv[2]

for i in range(duration):
    data_folder = base_folder + "/" + str(i)
    os.system("mkdir -p " + data_folder)
    os.system("free -m > " + data_folder + "/" + "free")
    os.system("cp /sys/kernel/mm/uksm/pages_* " + data_folder)
    time.sleep(1)
