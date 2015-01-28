import os

'''
@param filename : Name of the top file generated
@param keyword : Keyword for relevant data (eg : qemu-system)
'''
def dump_top_info(filename, keyword, load):
    dump_file = keyword + "-" + load + ".dump"
    os.system("cat " + filename + " | grep " + keyword + " >> " + dump_file)  

'''
@param filename : The dump file with information specific to load like qemu/lxc
@param n : Number of loads run during data collection. Each time "top" was run,
           it generated 'n' entries for the load (eg : 10 KVMs were run)
'''
def process_top_file(filename, load, n, container):
    l_count_file = "tmp-" + container + "-" + load + ".count"
    os.system("wc -l " + filename + ">" + l_count_file)
    l_count = open(l_count_file, "r")
    num_entries_str = l_count.readline()
    num_entries_str_arr = num_entries_str.split()
    num_entries_str = num_entries_str_arr[0]
    num_entries = int(num_entries_str)
    f = open(filename, 'r')
    time = 0
    data_file = "plot-data/" + container + "-" + load + "-top-mem-data.txt"
    data = open(data_file, "a")
    loop_count = num_entries/n
    for i in range(loop_count):
        total_mem_usage = 0
        for j in range(n):
            l = f.readline()
            tok = l.split()
            res = tok[5]
            if container == "kvm":
                res = res[:-1]
            RES = int(res)
            total_mem_usage = total_mem_usage + RES
        data_line = str(time) + " "
        time = time + 1
        data_line = data_line + str(total_mem_usage) + "\n"
        data.write(data_line)
    data.close()
    f.close()


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
