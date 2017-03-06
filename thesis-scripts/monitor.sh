#!/bin/sh

./startMonitoring.sh $1 &
./monitorMem.sh $1 &
./monitorIO.sh $1 
wait
cat cpuVal.txt | awk '{print $1, $2, $4}' > cpuv.txt
cat memVal.txt | awk '{print $1, $2, $5}' > memv.txt
cat ioVal.txt | awk '{print $1, $2, $4, $5}' > iov.txt
wait
rm cpuVal.txt
rm memVal.txt
rm ioVal.txt
AM=$1
RMR=$(expr $1 + 1)
sed '1,3d' cpuv.txt > cpuValt.txt
sed '1,3d' memv.txt > memValt.txt
sed '1,3d' iov.txt > ioValt.txt
sed '/Average:/d' cpuValt.txt > cpuVal.txt
sed '/Average:/d' memValt.txt > memVal.txt
sed '/Average:/d' ioValt.txt > ioVal.txt
wait
rm cpuValt.txt | rm memValt.txt | rm ioValt.txt
rm cpuv.txt | rm memv.txt | rm iov.txt
./convertCpu cpuVal.txt &
./convertMem memVal.txt &
./convertIOth ioVal.txt
wait
rm temp | rm temp1 | rm temp2
rm cpuVal.txt | rm memVal.txt | rm ioVal.txt
