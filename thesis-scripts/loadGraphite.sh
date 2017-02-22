#!/bin/bash

while read NAME;
do
  echo $NAME | nc localhost 2003
done < $1
