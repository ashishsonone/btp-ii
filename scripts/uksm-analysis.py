"""free output first two lines :-
                 total       used       free     shared    buffers     cached
    Mem:         24101       3526      20575          0        359        877
"""

import os, sys

num_folders = 0;
if(len(sys.argv) > 1):
    base_directories = []
    for i in range(2, len(sys.argv)):
        base_directories.append(sys.argv[i] + "/")
        num_folders = num_folders + 1

uksm_file = sys.argv[1]

def uksm(without_files_count, with_files_count):
    reference = []
    if(uksm_file == "pages_scanned"):
        for d in range(num_folders):
            f = open(base_directories[d] + "without" + "/0/" + uksm_file, 'r')
            line = f.readline()
            tokens = line.split()
            reference.append(int(tokens[0]))
    else:
        for d in range(num_folders):
            reference.append(0)

    time = 0;
    for i in range(without_files_count):
        aggr_value = 0
        for d in range(num_folders):
            f = open(base_directories[d] + "without" + "/"+ str(i)+ "/" + uksm_file, 'r')
            #read the second line. split and take the third token(i.e tokens[2])
            line = f.readline()
            tokens = line.split()
            aggr_value += (int(tokens[0]) - reference[d])
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
            aggr_value += (int(tokens[0]) - reference[d])
        print(str(time) + " " + str(aggr_value/num_folders))
        time = time + 1;

#uksm("pages_shared", 60, 600)
#uksm("pages_sharing", 60, 600)
uksm(180, 420)
