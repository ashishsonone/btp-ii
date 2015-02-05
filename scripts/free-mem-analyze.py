"""free output first two lines :-
                 total       used       free     shared    buffers     cached
    Mem:         24101       3526      20575          0        359        877
"""

import os, sys

if(len(sys.argv) > 1):
    base_directory = sys.argv[1] + "/"
else:
    base_directory = ""

free_file_name = "free"
without_directory = base_directory + "without"
with_directory = base_directory + "with"

without_files_count = len(os.listdir(without_directory))
with_files_count = len(os.listdir(with_directory))

time = 0;
for i in range(without_files_count-1): #one file is top file
    f = open(without_directory+"/"+str(i)+"/"+free_file_name, 'r')
    
    #read the second line. split and take the third token(i.e tokens[2])
    line = f.readline()
    line = f.readline()
    tokens = line.split()
    used_mem = int(tokens[2])
    cached_mem = int(tokens[6])
    print(str(time) + " " + str(used_mem-cached_mem))
    time = time + 1;

#print("switching...............")    

for i in range(with_files_count-1):
    f = open(with_directory+"/"+str(i)+"/"+free_file_name, 'r')
    
    #read the second line. split and take the third token(i.e tokens[2])
    line = f.readline()
    line = f.readline()
    tokens = line.split()
    used_mem = int(tokens[2])
    cached_mem = int(tokens[6])
    print(str(time) + " " + str(used_mem-cached_mem))
    time = time + 1

