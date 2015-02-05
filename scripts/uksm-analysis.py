"""free output first two lines :-
                 total       used       free     shared    buffers     cached
    Mem:         24101       3526      20575          0        359        877
"""

import os, sys

num_folders = -1;
if(len(sys.argv) > 1):
    base_directories = []
    for i in range(1, len(sys.argv)):
        base_directories.append(sys.argv[i] + "/")
        num_folders = num_folders + 1

def uksm(uksm_file, without_files_count, with_files_count):
    time = 0;
    for i in range(without_files_count):
        aggr_value = 0
        for d in range(num_folders):
            f = open(base_directories[d] + "without" + "/"+ str(i)+ "/" + uksm_file, 'r')
            #read the second line. split and take the third token(i.e tokens[2])
            line = f.readline()
            tokens = line.split()
            aggr_value += int(tokens[0])
        print(str(time) + " " + str(aggr_value/num_folders))
        time = time + 1;

    #print("switching...............")    
    for i in range(with_files_count):
        aggr_value = 0
        for d in range(num_folders):
            f = open(base_directories[d] + "with" + "/"+ str(i)+ "/" + uksm_file, 'r')
            #read the second line. split and take the third token(i.e tokens[2])
            line = f.readline()
            tokens = line.split()
            aggr_value += int(tokens[0])
        print(str(time) + " " + str(aggr_value/num_folders))
        time = time + 1;

uksm("pages_shared", 60, 600)
#uksm("pages_sharing")
