from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import numpy
import sys


def graph(datafile, graph_title, title1, title2 , xlabel, ylabel1, ylabel2, plotname):
    data1 = numpy.genfromtxt("plot-long-uksm-scanned/" + datafile, skip_header=0, names = ['timestamp','pages'])
    data2 = numpy.genfromtxt("plot-long-top-uksmd/" + datafile, skip_header=0, names = ['timestamp','percentage'])

    fig = plt.figure()
    host = host_subplot(111, axes_class=AA.Axes)
    plt.subplots_adjust(right=0.75)

    par1 = host.twinx()

    host.set_xlabel(xlabel)
    host.set_title(graph_title)    
    host.set_ylabel(ylabel1)
    host.set_ylim(0, 2500000)

    par1.set_ylabel(ylabel2)
    par1.set_ylim(0, 100)

    p1, = host.plot(data1['timestamp'], data1['pages'], c='r', label=title1)
    p2, = par1.plot(data2['timestamp'], data2['percentage'], c='g', label=title2)

    plt.annotate(
        "uksm starting", 
        xy = (data1['timestamp'][60], data1['pages'][60]), xytext = (100, -20),
        textcoords = 'offset points', ha = 'right', va = 'bottom',
        bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
        arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
    plt.annotate(
        "uksm starting", 
        xy = (data2['timestamp'][60], data2['percentage'][60]), xytext = (100, -20),
        textcoords = 'offset points', ha = 'right', va = 'bottom',
        bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
        arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))

    leg = host.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
                      fancybox=True, shadow=True, ncol=5)
	#plt.show()
    fig.savefig(plotname)
	#save("signal", ext="png", close=False, verbose=True)

#print(data['timestamp'])
graph("lxc-mysql.txt", "uksm page stats[lxc(10) + mysql]", "pages scanned", "uksm cpu usage",  "time(s)", "number of pages", "cpu usage(%)", "graph-lxc-mysql-cpu-scanned.png")
graph("lxc-apache.txt", "uksm page stats[lxc(10) + apache]", "pages scanned", "uksm cpu usage",  "time(s)", "number of pages", "cpu usage(%)", "graph-lxc-apache-cpu-scanned.png")
graph("kvm-mysql.txt", "uksm page stats[kvm(10) + mysql]", "pages scanned", "uksm cpu usage",  "time(s)", "number of pages", "cpu usage(%)", "graph-kvm-mysql-cpu-scanned.png")
graph("kvm-apache.txt", "uksm page stats[kvm(10) + apache]", "pages scanned", "uksm cpu usage",  "time(s)", "number of pages", "cpu usage(%)", "graph-kvm-apache-cpu-scanned.png")
#histogram(data )
#print(data['time_delta'])
