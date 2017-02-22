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
sed '1,3d' cpuv.txt > cpuVal.txt
sed '1,3d' memv.txt > memVal.txt
sed '1,3d' iov.txt > ioVal.txt
rm cpuv.txt | rm memv.txt | rm iov.txt
AM=$1
i="0"
while [ $i -lt $AM ] 
do
	if [ $i = "0" ]; then
		rm cpuMonitoring.txt
		rm diskMonitoring.txt
		rm memMonitoring.txt
	fi
	./convertCpu $(awk '{print $1, $2, $3}' cpuVal.txt) &
	./convertMem $(awk '{print $1, $2, $3}' memVal.txt) &
	./convertIOth $(awk '{print $1, $2, $3, $4}' ioVal.txt) &
	i=$(expr $i + 1)
done
wait
rm cpuVal.txt | rm memVal.txt | rm ioVal.txt