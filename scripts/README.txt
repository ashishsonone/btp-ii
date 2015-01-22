Run qemu in daemon mode:

sudo qemu-system-x86_64 -name t10 -m 256 -enable-kvm -smp 1 -drive file=/mnt/local/temp-mysql-10.qcow,if=none,id=drive-virtio-disk0,format=qcow2,cache=none -device virtio-blk-pci,drive=drive-virtio-disk0,id=virtio-disk0 -netdev tap,id=hostnet0,script=/etc/qemu-ifup,downscript=/etc/qemu-ifdown -device virtio-net-pci,netdev=hostnet0,id=net0,mac=40:54:00:cf:eb:22 -device virtio-balloon-pci,id=balloon0 -boot c -vga cirrus -monitor telnet:10.129.34.2:6536,server,nowait --daemonize -vnc 10.129.34.2:6532

to stop the running VM
	telnet 10.129.34.2 6536
	in telnet monitor: quit

quitting telnet session(without stopping VM) : use telnet way
	Ctrl+]
	telnet> quit   (//note the telnet> prompt)
