#!/bin/sh
sar -u 1 $1 > cpuVal.txt # -A specifies a specifik activity
