#!/bin/bash
COUNT=2
count=$(ping -c $COUNT $1 | grep 'received' | awk -F',' '{ print $2 }' | awk '{ print $1 }')
if [ $count -eq 0 ]; then
# 100% failed 
    echo "Host : $1 is down"
else
    echo "Host : $1 is up"
fi
