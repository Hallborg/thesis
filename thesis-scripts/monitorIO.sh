#!/bin/sh
sar -b 1 $1 > ioVal.txt # -A specifies a specifik activity

