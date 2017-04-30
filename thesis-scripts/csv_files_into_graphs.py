#!/usr/bin/env python2
""" Libraries used """
import numpy as np
import csv
import matplotlib.pyplot as plt
import sys
import os
import itertools
from os import listdir
from matplotlib.ticker import NullFormatter

""" Global variables """
ITERATION_CELLING=6
MAX_POINTS = 180
PEAK_SIZE = 19
CSV_AMOUNT=0
DEVICE_INDEX = 0
""" Mapping lists """
architecture = ['bm', 'docker', 'dockeriso', 'lxc']
clr = ['g', 'b', 'r', 'orange']
device=['cpu', 'disk-read', 'disk-write', 'receive', 'sent', 'amount_cass']
lb_operation=['create', 'delete', 'read', 'update']

""" Sets the global variables to the amount of files and min. """
def set_global_var(value):
	global CSV_AMOUNT
	CSV_AMOUNT = value
def set_global_var3(value):
	global DEVICE_INDEX
	DEVICE_INDEX = value

""" Collects path to the files and all file names. """
def get_path(extention=""):
	f = []
	real_path = str(os.path.dirname(os.path.realpath(__file__)))\
	+"/../csv-and-graphs/csv_files/%s" %(extention)
	return real_path

def find_csv_filenames(ext="cpu/bm/",suffix=""):
    filenames = listdir(get_path(extention=ext))
    return [ filename for filename in filenames if filename.startswith( suffix ) ]

""" Calculates mean value """
def mean_calc(a_list=[], amount=MAX_POINTS):
	return float(sum(a_list)) / amount

""" Extracts 300 data points from each file in architecture directory. """
def extract_data_points(reader):
	means = []
	nodes = [[], [], []]
	reader = list(reader)[5:]
	for row in reader:
		values = row[1:]
		i = 0
		for node_v in values:
			try:
				node_v = float(node_v)
			except ValueError as e:
				node_v = 0.0
			else:
				nodes[i].append(float(node_v))
			i = i + 1
	#print nodes
	for node in nodes:
		means.append(mean_calc(a_list=node))
	return float(mean_calc(a_list=means, amount=len(means)))

""" Reads files in device and architecture directories. """
def csv_to_list(path_to_dir, path_to_files, iteration):
	means_to_graph = []
	files = find_csv_filenames(ext=path_to_dir+"/"+path_to_files+"/", suffix=iteration)
	set_global_var(len(files))
	for i in range(0,CSV_AMOUNT):
		with open(str(get_path(extention=path_to_dir+"/"+path_to_files+"/"))+str(files[i]), 'r') as f:
			if 'amount_cass' in path_to_dir or 'comp-am' in path_to_dir:
				means = list(csv.reader(f))
			else:
				#print str(files[i])
				means = extract_data_points(csv.reader(f))
			means_to_graph.append(means)
	return means_to_graph

""" Continuous updating of anova """
def save_amount_to_anova(a_list, mon_comp):
	bm = a_list[0][0]
	docker = a_list[1][0]
	dockeriso = a_list[2][0]
	lxc = a_list[3][0]
	for i in range(0, len(lb_operation)):
		with open(str(get_path(extention="x_result/"))+mon_comp+"-"+lb_operation[i]+".csv", 'wb') as f: #'wb' 'ab'
			writer=csv.writer(f)
			writer.writerow(architecture)
			for j in range(0,5):
				writer.writerow([bm[j][i], docker[j][i], dockeriso[j][i], lxc[j][i]])

""" Continuous updating of anova """
def save_res_to_anova(a_list, mon_comp, index):
	if index == 1:
		for i in range(0, len(lb_operation)):
			with open(str(get_path(extention="x_result/"))+mon_comp+"-"+lb_operation[i]+".csv", 'wb') as f: #'wb' 'ab'
				writer=csv.writer(f)
				writer.writerow(architecture)
				writer.writerow([a_list[0][i], a_list[1][i], a_list[2][i], a_list[3][i]])
	else:
		for i in range(0, len(lb_operation)):
			with open(str(get_path(extention="x_result/"))+mon_comp+"-"+lb_operation[i]+".csv", 'ab') as f: #'wb' 'ab'
				writer=csv.writer(f)
				writer.writerow([a_list[0][i], a_list[1][i], a_list[2][i], a_list[3][i]])

def cross_validation_data(path_an_min):
	if device[5] in path_an_min[0]:
		global ITERATION_CELLING
		ITERATION_CELLING = 2
	for i in range(1, ITERATION_CELLING):
		means = []
		for op in architecture:
			print "Doing: %s for %s" % (path_an_min[0], op)
			means.append(csv_to_list(path_an_min[0], op, str(i)))
		if not means[0] or not means[1] or not means[2] or not means[3]:
			print "Nothing in the list"
		else:
			if device[5] in path_an_min[0]:
				save_amount_to_anova(means, path_an_min[0])
				pass
			else:
				save_res_to_anova(means, path_an_min[0], i)

def split_on_arch(a_list):
	bm = []
	docker = []
	dockeriso = []
	lxc = []
	i = 0
	for b_list in a_list:
		bmt = []
		dockert = []
		dockerisot = []
		lxct = []
		for c_list in b_list[1:]:
			bmt.append(float(c_list[0]))
			dockert.append(float(c_list[1]))
			dockerisot.append(float(c_list[2]))
			lxct.append(float(c_list[3]))
		bm.append(mean_calc(a_list=bmt, amount=len(bmt) ))
		docker.append(mean_calc(a_list=dockert, amount=len(dockert) ))
		dockeriso.append(mean_calc(a_list=dockerisot, amount=len(dockerisot) ))
		lxc.append(mean_calc(a_list=lxct, amount=len(lxct) ))
	return [bm, docker, dockeriso, lxc]

def read_cross_data(path, files):
	ret = []
	for name in files:
		with open(path+name, 'r') as f:
			ret.append(list(csv.reader(f)))
	return split_on_arch(ret)

""" Calculate y axis lenght. """
def calc_mean_std(m):
	to_ret= []
	for en in m:
		temp = ()
		for val in en:
			s = int(val)
			temp = temp +(s/3, )
		to_ret.append(temp)
	return to_ret

""" Appends bars from every file to the graph. """
def create_figs(means, lb, clrs, index, width, ax, i, delay, men_std):
	opacity = 0.65
	error_config = {'ecolor': '0.4'}
	rects = ax.bar(index-delay, means, width, 
		alpha=opacity, color=clrs, yerr=men_std,
		error_kw=error_config, label =lb)
	for rect in rects:
		height = rect.get_height()
		plt.text(rect.get_x() + rect.get_width()/2., 1.05*height,
			'%d' % int(height), ha='left', va='bottom')
	return delay

""" Configures the graph, plots the bars and displays the figure. """
def create_graphs(means=[], std_mean=(), graph_type="cpu-bars", xlabel="Operation", 
	ylabel="percent (%)", title="CPU intensive write/read/update/delete load in percent", 
	xtick=('Create', 'Delete', 'Read', 'Update')):
	index = np.arange(len(means[0]))
	width = 0.15
	i = 0
	fig, ax = plt.subplots(1,1, figsize=(18, 6), facecolor='w', edgecolor='k') # 
	fig.subplots_adjust(hspace = .5, wspace=.001)
	delay = 0
	for m in means:
		delay = create_figs(m, architecture[i], clr[i], index, width, ax, i, delay, std_mean[i])
		i=i+1
		delay = delay-width
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.title(title)
	placement = index + width + width/2
	plt.xticks(placement, xtick)
	plt.legend(loc=1, bbox_to_anchor=(1.1, 1.0))
	plt.savefig(str(get_path(extention="z_graphs/"))+graph_type+".png", dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None)

def handle_graphs(mean_val, name):
	if device[3] in name or device[4] in name:
		create_graphs(means=mean_val, std_mean=calc_mean_std(mean_val), graph_type=name+'-bars',
			ylabel='kb/s', title='Network I/O intensive write/read/update/delete load in kb/s')
	elif device[0] in name:
		create_graphs(means=mean_val, std_mean=calc_mean_std(mean_val))
	elif device[1] in name or device[2] in name:
		create_graphs(means=mean_val, std_mean=calc_mean_std(mean_val), graph_type=name+'bars',
		 ylabel='mb/s', title='I/O intensive write/read/update/delete load in mb/s')
	elif 'amount_cass' in name:
		create_graphs(means=mean_val, std_mean=calc_mean_std(mean_val), graph_type=name+'-bars', ylabel='#edrs',
			title='Amount of edrs handled in each operation')
		pass
	elif 'comp-am' in name:
		pass

def handle_files(path_an_min):
	cross_validation_data(path_an_min)
	means_val = read_cross_data(get_path(extention="x_result/"), find_csv_filenames(ext="x_result/", suffix=path_an_min[0]))
	print path_an_min
	print means_val
	handle_graphs(means_val, str(path_an_min[0]))

""" Handle agruments in  """
def handle_argvs(argv):
	try:
		argv[0] = str(argv[0])
	except ValueError as e:
		print "Usage: ./lineGraphGen.py <extend the directory(cpu, write-read, memory)>\
		 <Integer (min value where something happens)> <Integer (1 bars, 2 line)>"
		exit()
	else:
		if '-h' in argv[0]:
			print "Usage: ./lineGraphGen.py <extend the directory(cpu, write-read, memory)>\
		 	<Integer (min value where something happens)> <Integer (1 bars, 2 line)>"
		 	exit()
		try:
			argv[1] = int(argv[1])
		except ValueError as e:
			print "Usage: ./lineGraphGen.py <extend the directory(cpu, write-read, memory)>\
		 <Integer (1 bars, 2 line)> <FLoat (values from a certain point)>"
			exit()
		else:
			if argv[1] == 1 or argv[1] == 2:
				return [argv[0], argv[1]]

""" Main window. """
def main(argv):
	path_n_min = handle_argvs(argv)
	for i in range(0, len(device)):
		if str(path_n_min[0]) in device[i]:
			set_global_var3(i)
	if path_n_min[1] == 1:
		handle_files(path_n_min)
	elif path_n_min[1] == 2:
		handle_n_create_lines(path_n_min)
	else:
		print 'Wrong option typ -h for help.'

""" Start. """
if __name__ == "__main__":
	main(sys.argv[1:3])