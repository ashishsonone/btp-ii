Run qemu in daemon mode:

sudo qemu-system-x86_64 -name t10 -m 256 -enable-kvm -smp 1 -drive file=/mnt/local/temp-mysql-10.qcow,if=none,id=drive-virtio-disk0,format=qcow2,cache=none -device virtio-blk-pci,drive=drive-virtio-disk0,id=virtio-disk0 -netdev tap,id=hostnet0,script=/etc/qemu-ifup,downscript=/etc/qemu-ifdown -device virtio-net-pci,netdev=hostnet0,id=net0,mac=40:54:00:cf:eb:22 -device virtio-balloon-pci,id=balloon0 -boot c -vga cirrus -monitor telnet:10.129.34.2:6536,server,nowait --daemonize -vnc 10.129.34.2:6532

=====================================================

to stop the running VM
	telnet 10.129.34.2 6536
	in telnet monitor: quit

=====================================================

quitting telnet session(without stopping VM) : use telnet way
	Ctrl+]
	telnet> quit   (//note the telnet> prompt)

=====================================================

Find the ips being used(by hosts that are up)
sudo nmap -sP 10.129.34.2/24

=====================================================

Clear the cache memory:
free -m   //before cached = 21770 MB
sudo sh -c "sync; echo 3 > /proc/sys/vm/drop_caches"
free -m   //after cached = 18 MB only :)

=====================================================

Universally administered and locally administered addresses are distinguished by setting the second-least-significant bit of the most significant byte of the address. If the bit is 0, the address is universally administered. If it is 1, the address is locally administered.
There are actually 4 sets of Locally Administered Address Ranges that can be used on your network without fear of conflict, assuming no one else has assigned these on your network:

x2-xx-xx-xx-xx-xx
x6-xx-xx-xx-xx-xx
xA-xx-xx-xx-xx-xx
xE-xx-xx-xx-xx-xx

So for our experiments - 
a. mysql : 42:54:00:cf:eb:00 , 01, 02, ....  | telent 6500, 6501, ....  | vnc 6600, 6601, ....
b. apache : 42:54:00:cf:ec:00, 01, 02, ....  | telnet 6700, 6701, ....  | vnc 6800, 6801, ....

======================================================

mysql one time setup for static ip(look at what is assigned by dhcp and assign it as static)

sudo qemu-system-x86_64 -name t0 -m 256 -enable-kvm -smp 1 -drive file=/mnt/local/temp-mysql-0.qcow,if=none,id=drive-virtio-disk0,format=qcow2,cache=none -device virtio-blk-pci,drive=drive-virtio-disk0,id=virtio-disk0 -netdev tap,id=hostnet0,script=/etc/qemu-ifup,downscript=/etc/qemu-ifdown -device virtio-net-pci,netdev=hostnet0,id=net0,mac=42:54:00:cf:eb:00 -device virtio-balloon-pci,id=balloon0 -boot c -vga cirrus -monitor telnet:10.129.34.2:6500,server,nowait -monitor stdio

once ip assigned use following command to run in daemon mode[specify SAME mac address]

sudo qemu-system-x86_64 -name t0 -m 256 -enable-kvm -smp 1 -drive file=/mnt/local/temp-mysql-0.qcow,if=none,id=drive-virtio-disk0,format=qcow2,cache=none -device virtio-blk-pci,drive=drive-virtio-disk0,id=virtio-disk0 -netdev tap,id=hostnet0,script=/etc/qemu-ifup,downscript=/etc/qemu-ifdown -device virtio-net-pci,netdev=hostnet0,id=net0,mac=42:54:00:cf:eb:00 -device virtio-balloon-pci,id=balloon0 -boot c -vga cirrus -monitor telnet:10.129.34.2:6500,server,nowait -monitor stdio -vnc 10.129.34.2:6600 --daemonize


======================================================

/etc/network/interfaces

auto eth0
iface eth0 inet static
address 10.129.28.58
netmask 255.255.128.0
gateway 10.129.1.250
======================================================
mysql-0 : 42:54:00:cf:eb:00 : 10.129.28.58
mysql-1 : 42:54:00:cf:eb:01 : 10.129.28.236
mysql-2 : 42:54:00:cf:eb:02 : 10.129.26.144
mysql-3 : 42:54:00:cf:eb:03 : 10.129.28.234
mysql-4 : 42:54:00:cf:eb:04 : 10.129.28.77
mysql-5 : 42:54:00:cf:eb:05 : 10.129.26.43
mysql-6 : 42:54:00:cf:eb:06 : 10.129.26.31
mysql-7 : 42:54:00:cf:eb:07 : 10.129.26.72
mysql-8 : 42:54:00:cf:eb:08 : 10.129.26.251
mysql-9 : 42:54:00:cf:eb:09 : 10.129.26.61
mysql-10 : 42:54:00:cf:eb:10 : 10.129.28.82
mysql-11 : 42:54:00:cf:eb:11 : 10.129.28.225
mysql-12 : 42:54:00:cf:eb:12 : 10.129.28.90
mysql-13 : 42:54:00:cf:eb:13 : 10.129.26.211
mysql-14 : 42:54:00:cf:eb:14 : 10.129.26.190


======================================================
lxc containers mysql
mysql-0  10.129.28.81
mysql-1  10.129.26.102 
mysql-2  10.129.28.104
mysql-3  10.129.28.123
mysql-4  10.129.26.98
mysql-5  10.129.28.170
mysql-6  10.129.28.181
mysql-7  10.129.26.252
mysql-8  10.129.26.177
mysql-9  10.129.26.88
