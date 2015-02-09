import os,sys

machines = ["kvm", "lxc"]
loads = ["apache", "mysql", "mix"]
data_field = ["pages_shared", "pages_scanned", "pages_sharing"]

input_dir = sys.argv[1]
output_dir = sys.argv[2]


os.system("mkdir -p " + output_dir)

for m in machines:
  for l in loads:
    output_folder = output_dir + "/" + m + "-" + l
    os.system("mkdir -p " + output_folder)
    f1 = input_dir + "/" + "exp0-" + m + "-" + l
    f2 = input_dir + "/" + "exp1-" + m + "-" + l
    f3 = input_dir + "/" + "exp2-" + m + "-" + l
    for d in data_field:
      os.system("python uksm-analysis.py " + d + " " + f1 + " " + f2 + " " + f3 + " > " + output_folder + "/" + "uksm-" + d + ".txt")
