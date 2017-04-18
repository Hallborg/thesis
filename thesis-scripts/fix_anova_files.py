#!/usr/bin/env python2
import csv
import sys
import os
from os import listdir

architecture = ['BM', 'Docker', 'DockerIso', 'LXC']
device=['cpu', 'sent', 'recive']
lb_operation=['write', 'read', 'update', 'delete']
dir_path ="%s/../csv-and-graphs/anova/csv/" % (str(os.path.dirname(os.path.realpath(__file__))))

def find_csv_filenames( path_to_dir=dir_path, suffix=".csv" ):
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]

def read_files(direc=dir_path, filenames=[]):
	data_by_operations = []
	i = 0
	for filename in filenames:
		temp = []
		temp.append(architecture[i])
		with open(str(direc)+str(filename), 'r') as f:
			spamreader = csv.reader(f, delimiter=',', quotechar='|')
			for row in spamreader:
				temp.extend(row)
		data_by_operations.append(temp)
		i = i + 1
	return data_by_operations

def make_one_file(a_list, dev, operand):
	headers = []
	for aa_list in a_list:
		headers.append(aa_list[0])
	bm = a_list[0]
	strl = len(bm)
	docker = a_list[1]
	if len(docker) is not strl: print "NOO"
	docker_iso = a_list[2]
	if len(docker_iso) is not strl: print "NOO"
	lxc = a_list[3]
	if len(lxc) is not strl: print "NOO"
	with open(str(dir_path)+'done/'+dev+'-'+operand+'.csv', 'wb') as f:
		writer=csv.writer(f)
		for i in range(0, strl-1):
			writer.writerow([bm[i], docker[i], docker_iso[i], lxc[i]])

def handle_data(a_list):
	i = 0; j = 0
	for dev_oper in a_list:
		#print dev_oper
		make_one_file(dev_oper, device[i], lb_operation[j])
		if j < 3:
			j = j + 1
		else:
			j = 0
			i = i + 1

def read_directory():
	files_data = []
	for dev in device:
		for oper in lb_operation:
			files_data.append(read_files(filenames=find_csv_filenames(suffix=str('-'+dev+'-'+oper+'.csv'))))
	handle_data(files_data)

read_directory()