from matplotlib import pyplot as plt
import numpy
import sys


def graph(datafile, graph_title, title1, title2 , xlabel, ylabel, plotname):
        data1 = numpy.genfromtxt("plot-long-uksm-shared/" + datafile, skip_header=0, names = ['timestamp','pages'])
        data2 = numpy.genfromtxt("plot-long-uksm-sharing/" + datafile, skip_header=0, names = ['timestamp','pages'])
	fig = plt.figure()
	ax1 = fig.add_subplot(111)

	ax1.set_title(graph_title)    
	ax1.set_xlabel(xlabel)
	ax1.set_ylabel(ylabel)

	ax1.plot(data1['timestamp'], data1['pages'], c='r', label=title1)
	ax1.plot(data2['timestamp'], data2['pages'], c='g', label=title2)
        plt.annotate(
            "uksm starting", 
            xy = (data1['timestamp'][60], data1['pages'][60]), xytext = (100, -20),
            textcoords = 'offset points', ha = 'right', va = 'bottom',
            bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
            arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
        plt.annotate(
            "uksm starting", 
            xy = (data2['timestamp'][60], data2['pages'][60]), xytext = (100, -20),
            textcoords = 'offset points', ha = 'right', va = 'bottom',
            bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
            arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))

	leg = ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
                          fancybox=True, shadow=True, ncol=5)
	#plt.show()
        fig.savefig(plotname)
	#save("signal", ext="png", close=False, verbose=True)

#print(data['timestamp'])
graph("lxc-mysql.txt", "uksm page stats[lxc(10) + mysql]", "pages shared", "pages sharing",  "time(s)", "number of pages", "graph-lxc-mysql-share.png")
graph("lxc-apache.txt", "uksm page stats[lxc(10) + apache]", "pages shared", "pages sharing",  "time(s)", "number of pages", "graph-lxc-apache-share.png")

graph("kvm-mysql.txt", "uksm page stats[kvm(10) + mysql]", "pages shared", "pages sharing",  "time(s)", "number of pages", "graph-kvm-mysql-share.png")
graph("kvm-apache.txt", "uksm page stats[kvm(10) + apache]", "pages shared", "pages sharing",  "time(s)", "number of pages", "graph-kvm-apache-share.png")
#histogram(data )
#print(data['time_delta'])
