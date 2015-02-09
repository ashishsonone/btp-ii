import os, sys

num_folders = 0;
if(len(sys.argv) > 1):
    directories = []
    for i in range(1, len(sys.argv)):
        directories.append(sys.argv[i] + "/")
        num_folders = num_folders + 1

'''
@param filename : Name of the top file generated
@param keyword : Keyword for relevant data (eg : qemu-system)
'''
def dump_top_info(keyword):
    #remove old dump files
    for i in range(num_folders):
        dump_file = "dump" + str(i) + ".dump"
        os.system("cat " + directories[i] + "/without/top | grep " + keyword + " > " + dump_file)
        os.system("cat " + directories[i] + "/with/top | grep " + keyword + " >> " + dump_file)

'''
@param filename : The dump file with information specific to load like qemu/lxc
@param n : Number of loads run during data collection. Each time "top" was run,
           it generated 'n' entries for the load (eg : 10 KVMs were run)
'''
def process_top_file(n, col_no, seconds):
    dump_files = []
    for i in range(num_folders):
        dump_file = "dump" + str(i) + ".dump"
        f = open(dump_file, 'r')
        dump_files.append(f)

    time = 0
    for i in range(seconds):
        total_mem_usage = 0
        for d in range(num_folders):
            sub_total = 0
            for j in range(n):
                l = dump_files[d].readline()
                tok = l.split()
                res = tok[col_no]
                #if container == "kvm":
                #    res = res[:-1]
                RES = int(res)
                sub_total = sub_total + RES
            total_mem_usage = total_mem_usage + sub_total
        print(str(time) + " " + str(total_mem_usage/num_folders))
        time = time + 1

    for i in range(num_folders):
        dump_files[i].close()

"""
dump_top_info("data-kvm-apache-10/without/top", "qemu-system", "apache")    
dump_top_info("data-kvm-apache-10/with/top", "qemu-system", "apache")    
process_top_file("qemu-system-apache.dump", "apache", 10, "kvm")

dump_top_info("data-kvm-mysql-10/without/top", "qemu-system", "mysql")    
dump_top_info("data-kvm-mysql-10/with/top", "qemu-system", "mysql")    
process_top_file("qemu-system-mysql.dump", "mysql", 10, "kvm")

dump_top_info("data-lxc-apache-10/without/top", "lxc-start", "apache")    
dump_top_info("data-lxc-apache-10/with/top", "lxc-start", "apache")    
process_top_file("lxc-start-apache.dump", "apache", 10, "lxc")

dump_top_info("data-lxc-mysql-10/without/top", "lxc-start", "mysql")    
dump_top_info("data-lxc-mysql-10/with/top", "lxc-start", "mysql")    
process_top_file("lxc-start-mysql.dump", "mysql", 10, "lxc")
"""

dump_top_info("uksmd")
process_top_file(1, 8, 180 + 420)
