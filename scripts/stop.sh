ps -e | grep qemu
telnet 10.129.34.2 6536 <<EOF
quit
EOF
sleep 1;
ps -e | grep qemu
