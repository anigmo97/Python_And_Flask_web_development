#!/bin/bash
#sudo lsof -i:8000 # get info of process using port 8000
PIDS="$(lsof -i:8000 | awk '{ if ($2!= "PID") print $2 }' | tr '\n' ' ')" 
echo $PIDS
kill -9 $PIDS
