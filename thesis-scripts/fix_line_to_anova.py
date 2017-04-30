#!/usr/bin/env python2
import csv
import sys
import os
from os import listdir


architecture = ['BM', 'Docker', 'LXC', 'DockerIso']
lb_operation=['delete', 'read', 'update', 'write']
dir_path ="%s/../csv-and-graphs/anova/lines/" % (str(os.path.dirname(os.path.realpath(__file__))))


def find_csv_filenames(path_to_dir=dir_path, suffix=".csv"):
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.startswith( suffix ) ]

def read_files(direc=dir_path, filenames=[], index=0):
	data_by_operations = []
	print filenames
	#data_by_operations.append([architecture[index]])
	for filename in filenames:
		temp = []
		#temp.append(architecture[i])
		with open(str(direc)+str(filename), 'r') as f:
			spamreader = csv.reader(f, delimiter=',', quotechar='|')
			for row in spamreader:
				#print spamreader
				temp.extend(row)
		temp.pop(len(temp)-1)
		data_by_operations.append(temp)
		#i = i + 1
	return data_by_operations

def handle_data(a_list):
	print len(a_list)
	bm = a_list[0]
	docker = a_list[1]
	lxc = a_list[2]
	dockeriso = a_list[3]
	for i in range(0, len(bm)):
		bm_t = bm[i]
		docker_t = docker[i]
		lxc_t = lxc[i]
		dockeriso_t = dockeriso[i]
		with open(str(dir_path)+'done/'+lb_operation[i]+'.csv', 'wb') as f:
			writer=csv.writer(f)
			writer.writerow(architecture)
			for j in range(0, len(bm_t)):
				writer.writerow([str(bm_t[j]).replace(' ',''), str(docker_t[j]).replace(' ',''),
				 str(lxc_t[j]).replace(' ',''), str(dockeriso_t[j]).replace(' ','')])

def read_directory():
	files_data = []
	i = 0
	for arch in architecture:
		files_data.append(read_files(filenames=find_csv_filenames(suffix=str(arch+'-')), index=i))
		i = i + 1
	handle_data(files_data)

read_directory()