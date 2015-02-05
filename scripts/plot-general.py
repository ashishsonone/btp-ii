from matplotlib import pyplot as plt
import numpy
import sys


def graph(datafile, title, xlabel, ylabel, plotname):
        data = numpy.genfromtxt(datafile, skip_header=0, names = ['timestamp','memory'])
	fig = plt.figure()
	ax1 = fig.add_subplot(111)

	ax1.set_title(title)    
	ax1.set_xlabel(xlabel)
	ax1.set_ylabel(ylabel)

	ax1.plot(data['timestamp'], data['memory'], c='r', label=title)

	leg = ax1.legend()
	#plt.show()
        fig.savefig(plotname)
	#save("signal", ext="png", close=False, verbose=True)

#print(data['timestamp'])
graph("lxc-uksmd-mysql-top-mem-data.txt", "uksmd cpu usage vs time[lxc(10) + mysql]", "time(s)", "cpu usage(%)", "plot-uksmd-lxc-mysql-top.png")
graph("lxc-uksmd-apache-top-mem-data.txt", "uksmd cpu usage vs time[lxc(10) + apache]", "time(s)", "cpu usage(%)", "plot-uksmd-lxc-apache-top.png")
graph("kvm-uksmd-mysql-top-mem-data.txt", "uksmd cpu usage vs time[kvm(10) + mysql]", "time(s)", "cpu usage(%)", "plot-uksmd-kvm-mysql-top.png")
graph("kvm-uksmd-apache-top-mem-data.txt", "uksmd cpu usage vs time[kvm(10) + apache]", "time(s)", "cpu usage(%)", "plot-uksmd-kvm-apache-top.png")
#histogram(data )
#print(data['time_delta'])
