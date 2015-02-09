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
        plt.annotate(
            "uksm starting", 
            xy = (data['timestamp'][60], data['memory'][60]), xytext = (100, -20),
            textcoords = 'offset points', ha = 'right', va = 'bottom',
            bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
            arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))

	leg = ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
                          fancybox=True, shadow=True, ncol=5)
	#plt.show()
        fig.savefig(plotname)
	#save("signal", ext="png", close=False, verbose=True)

#print(data['timestamp'])
graph("lxc-mysql.txt", "system memory usage vs time[lxc(10) + mysql]", "time(s)", "memory used(MB)", "graph-lxc-mysql-used.png")
graph("lxc-apache.txt", "system memory usage vs time[lxc(10) + apache]", "time(s)", "memory used(MB)", "graph-lxc-apache-used.png")
graph("kvm-mysql.txt", "system memory usage vs time[kvm(10) + mysql]", "time(s)", "memory used(MB)", "graph-kvm-mysql-used.png")
graph("kvm-apache.txt", "system memory usage vs time[kvm(10) + apache]", "time(s)", "memory used(MB)", "graph-kvm-apache-used.png")
#histogram(data )
#print(data['time_delta'])
