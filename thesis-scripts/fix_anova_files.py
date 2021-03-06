#!/usr/bin/env python2
import csv
import sys
import os
from os import listdir

architecture = ['BM', 'Docker', 'LXC', 'DockerIso']
device=['cpu', 'sent', 'recive']
device2=['cpu', 'sent']
lb_operation=['write', 'read', 'update', 'delete']
dir_path ="%s/../csv-and-graphs/anova/csv/" % (str(os.path.dirname(os.path.realpath(__file__))))
dir_path2 = "%s/../csv-and-graphs/anova/comp-csv/" % (str(os.path.dirname(os.path.realpath(__file__))))

def find_csv_filenames(path_to_dir=dir_path, suffix=".csv"):
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

def make_one_file(a_list, dev, operand, dire):
	headers = []
	for aa_list in a_list:
		headers.append(aa_list[0])
	bm = a_list[0]
	strl = len(bm)
	docker = a_list[1]
	if int(len(docker)) < int(strl): print "Docker: %d smaller then bm: %d" % (int(len(docker)), int(strl))
	if int(len(docker)) > int(strl): print "Docker: %d bigger then bm: %d" % (int(len(docker)), int(strl))
	if int(len(docker)) == int(strl): print "Docker: %d same as bm: %d" % (int(len(docker)), int(strl))
	docker_iso = a_list[2]
	if int(len(docker_iso)) < int(strl): print "ISO docker: %d smaller then bm: %d" % (int(len(docker_iso)), int(strl))
	if int(len(docker_iso)) > int(strl): print "ISO docker: %d bigger then bm: %d" % (int(len(docker_iso)), int(strl))
	if int(len(docker_iso)) == int(strl): print "ISO docker: %d same as bm: %d" % (int(len(docker_iso)), int(strl))
	lxc = a_list[3]
	if int(len(lxc)) < int(strl): print "LXC: %d smaller then bm: %d" % (int(len(lxc)), int(strl))
	if int(len(lxc)) > int(strl): print "LXC: %d bigger then bm: %d" % (int(len(lxc)), int(strl))
	if int(len(lxc)) == int(strl): print "LXC: %d same as bm: %d" % (int(len(lxc)), int(strl))
	with open(str(dire)+'done/'+dev+'-'+operand+'.csv', 'wb') as f:
		writer=csv.writer(f)
		for i in range(0, strl-1):
			writer.writerow([bm[i], docker[i], docker_iso[i], lxc[i]])
			if 'read' in operand:
				print "BM: %s  ,  D: %s  ,  DI: %s  ,  LXC: %s " % (bm[i], docker[i], docker_iso[i], lxc[i])

def handle_data(a_list, t):
	i = 0; j = 0
	for dev_oper in a_list:
		if t == 1:
			print "[%s] operation for [%s] takes place!" % (lb_operation[j], device[i])
			make_one_file(dev_oper, device[i], lb_operation[j], dir_path)
		elif t == 2:
			print "[%s] operation for [%s] takes place!" % (lb_operation[j], device2[i])
			make_one_file(dev_oper, device2[i], lb_operation[j], dir_path2)
		if j < 3:
			j = j + 1
		else:
			j = 0
			i = i + 1
		print '\n'

def read_directory(t):
	files_data = []
	for dev in device:
		for oper in lb_operation:
			if t == 1:
				files_data.append(read_files(filenames=find_csv_filenames(suffix=str('-'+dev+'-'+oper+'.csv'))))
			elif t ==2:
				files_data.append(read_files(direc=dir_path2,filenames=find_csv_filenames(path_to_dir=dir_path2, suffix=str('-'+dev+'-'+oper+'.csv'))))
	handle_data(files_data, t)


def main(argv):
	try:
		int(argv[0])
	except TypeError as e:
		print "Only Integer!"
		exit()
	else:
		read_directory(int(argv[0]))



if __name__ == "__main__":
	main(sys.argv[1:2])





