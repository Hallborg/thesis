#!/usr/bin/env python2
#import sys
#import subprocess
#import os
#import affinity
import random

def createList():
	return [random.randrange(1, int(sys.argv[1]),1) for _ in range(int(sys.argv[1]))]
def mean_calc(a_list=createList()):
	return float(sum(a_list)) / max(len(a_list), 1)
print mean_calc()


#print dir(os)   #len(os.sched_getaffinity(0))
#bash_restrict_command = "taskset -c 0 "
#service_command ="systemctl start cassandra" #"python2 data-generator.py "
#bash_command = "%s%s" %(bash_restrict_command, service_command)
#pid = os.getpid()
#print pid
#s = affinity.get_process_affinity_mask(pid)
#process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE, shell=True)
#output, error = process.communicate()
#print output
#print error

