import os, sys

num_folders = 0;
if(len(sys.argv) > 1):
    directories = []
    for i in range(2, len(sys.argv)):
        directories.append(sys.argv[i])
        num_folders = num_folders + 1

def getData(folder,  entry_num):
  avg = 0
  data_file = sys.argv[1]
  if data_file == "free":
    for i in range(num_folders):
      #read the second line. split and take the third token(i.e tokens[2])
      cur_dir = directories[i] + "/" + folder
      filename = cur_dir + "/" + str(entry_num) + "/" + sys.argv[1]
      f = open(filename, "r")
      line = f.readline()
      line = f.readline()
      tokens = line.split()
      used_mem = int(tokens[2])
      cached_mem = int(tokens[6])
      avg += (used_mem - cached_mem)

  else:
    for i in range(num_folders):
      cur_dir = directories[i] + "/" + folder
      filename = cur_dir + "/" + str(entry_num) + "/" + sys.argv[1]
      f = open(filename, "r")
      line = f.readline()
      avg = avg + int(line)
  avg = avg*1.0/num_folders
  #print(str(avg) + " ++++++++++++++++++++++++++ ")
  avg = round(avg,3)
  print(folder + " " + data_file + " "+ str(avg))

getData("idle", 4)
getData("without", 179)
getData("with",  419)

