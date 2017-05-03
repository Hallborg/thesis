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
MAX_POINTS=180
PEAK_SIZE=20
CSV_AMOUNT=0
DEVICE_INDEX=0
MIN_VALUE_ACCEPTED=3.5
""" Mapping lists """
architecture = ['bm', 'docker', 'dockeriso', 'lxc']
clr = ['g', 'b', 'r', 'orange']
device=['cpu', 'disk-read', 'disk-write', 'receive', 'sent', 'amount_c', 'v_step']
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

	for node in nodes:
		if len(node) > 0.1:
			means.append(mean_calc(a_list=node))
	return float(mean_calc(a_list=means, amount=len(means)))

def to_float(a_list):
	ret = []
	for s in a_list:
		ret.append(float(s))
	return ret

def filter_am(a_list, b_list):
	temp = 0
	for i in range(1, len(a_list)):
		if a_list[i] < a_list[temp]:
			temp = i
	a_list.pop(temp)
	b_list.pop(temp)
	return a_list, b_list

"""  """
def extract_data_points_step(reader, name, it):
	if 'disk_' in it:
		global MIN_VALUE_ACCEPTED
		MIN_VALUE_ACCEPTED=11.0
	times = 0
	peak_means = []
	time_frame = []
	reader = list(reader)[4:]
	iterations = 1
	temp = []
	for row in reader:
		future_row = reader[iterations]
		future_row = future_row[1:]
		future_row = to_float(future_row)
		row = row[1:]
		row = to_float(row)
		if float(mean_calc(a_list=row, amount=len(row))) > MIN_VALUE_ACCEPTED:
			temp.append(mean_calc(a_list=row, amount=len(row)))
			times = times + 1
			if float(mean_calc(a_list=future_row, amount=len(future_row))) < MIN_VALUE_ACCEPTED:
				if 'disk_' in it:
					if len(temp) > 2:
						itere = 0
						for t in temp:
							if t < 100:
								#print "hje"
								temp.pop(itere)
							itere = itere +1
				peak_means.append(mean_calc(a_list=temp, amount=len(temp)))
				time_frame.append(times)
				times = 0
				temp = []
		if iterations < len(reader)-1:
			iterations = iterations + 1
	while len(peak_means) > PEAK_SIZE:
		peak_means, time_frame = filter_am(peak_means, time_frame)
	return peak_means, time_frame
	

""" Reads files in device and architecture directories. """
def csv_to_list(path_to_dir, path_to_files, iteration):
	means_to_graph = []
	times_to_graph = []
	files = find_csv_filenames(ext=path_to_dir+"/"+path_to_files+"/", suffix=iteration)
	set_global_var(len(files))
	for i in range(0,CSV_AMOUNT):
		with open(str(get_path(extention=path_to_dir+"/"+path_to_files+"/"))+str(files[i]), 'r') as f:
			if 'amount_c' in path_to_dir or 'comp-am' in path_to_dir:
				means = list(csv.reader(f))
				means_to_graph.append(means)
			elif device[6] in path_to_dir:
				#print files[i]
				means, times = extract_data_points_step(csv.reader(f), files[i], iteration)
				means_to_graph = means
				times_to_graph = times
			else:
				means = extract_data_points(csv.reader(f))
				means_to_graph.append(means)
	if device[6] in path_to_dir:
		return means_to_graph, times_to_graph
	else:
		return means_to_graph

"""  """
def save_step_to_anova(a_list, mon_comp):
	with open(str(get_path(extention="x_result/"))+mon_comp+".csv", 'wb') as f: #'wb' 'ab'
		writer=csv.writer(f)
		writer.writerow(architecture)
		for i in range(0, PEAK_SIZE):
			writer.writerow([a_list[0][i], a_list[1][i], a_list[2][i], a_list[3][i]])

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

#def handle_line(name):
#	pass
"""  """
def cross_validation_data(path_an_min):
	toRet = []
	toRet2= []
	step = ['cpu_', 'disk_']
	if device[5] in path_an_min[0] or 'comp_' in path_an_min[0]:
		global ITERATION_CELLING
		ITERATION_CELLING = 2
	elif device[6] in path_an_min[0]:
		global ITERATION_CELLING
		ITERATION_CELLING = 3
	for i in range(1, ITERATION_CELLING):
		means = []
		times = []
		for op in architecture:
			print "Doing: %s for %s" % (path_an_min[0], op)
			if device[6] in path_an_min[0]:
				m, t = csv_to_list(path_an_min[0], op, str(step[i-1]))
				means.append(m)
				times.append(t)
			else:
				means.append(csv_to_list(path_an_min[0], op, str(i)))
		#print means[0], len(means)
		#print times, len(times)
		if not means[0] or not means[1] or not means[2] or not means[3]:
			print "Nothing in the list"
		else:
			if device[5] in path_an_min[0]:
				save_amount_to_anova(means, path_an_min[0])
			elif device[6] in path_an_min[0]:
				save_step_to_anova(means, str(path_an_min[0])+"-"+str(step[i-1]))
				save_step_to_anova(times, str(path_an_min[0])+"-"+str(step[i-1])+"-times")
				toRet.append(means)
				toRet2.append(times)
			else:
				save_res_to_anova(means, path_an_min[0], i)
	if 'v_step' in path_an_min[0]:
		return toRet, toRet2
	else:
		return [], []

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
		plt.text(float(rect.get_x()) + rect.get_width()/2., 1.05*height+i/2,
			'%d' % int(height), ha='left', va='bottom')
	return delay

""" Configures the graph, plots the bars and displays the figure. """
def create_graphs(means=[], std_mean=(), graph_type="cpu-bars", xlabel="Operation", 
	ylabel="percent (%)", title="CPU intensive write/read/update/delete load in percent", 
	xtick=('Create', 'Delete', 'Read', 'Update')):
	index = np.arange(len(means[0]))
	width = 0.20
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
	plt.legend(loc=1, bbox_to_anchor=(1.0, 1.0))
	plt.savefig(str(get_path(extention="z_graphs/"))+graph_type+".png", dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None)

def handle_graphs(mean_val, name):
	if device[3] in name or device[4] in name:
		create_graphs(means=mean_val, std_mean=calc_mean_std(mean_val), graph_type=name+'-bars',
			ylabel='kb/s', title='Network I/O intensive write/read/update/delete load in kb/s')
	elif 'comp_cpu' in name:
		create_graphs(means=mean_val, std_mean=calc_mean_std(mean_val), graph_type=name+'-bars')
	elif device[0] in name:
		create_graphs(means=mean_val, std_mean=calc_mean_std(mean_val))
	elif device[1] in name or device[2] in name:
		create_graphs(means=mean_val, std_mean=calc_mean_std(mean_val), graph_type=name+'bars',
		 ylabel='mb/s', title='I/O intensive write/read/update/delete load in mb/s')
	elif 'amount_c' in name:
		create_graphs(means=mean_val, std_mean=calc_mean_std(mean_val), graph_type=name+'-bars', ylabel='#edrs',
			title='Amount of edrs handled in each operation')
		pass
	elif 'comp-am' in name:
		pass

def calc_x_axis(ls):
	amount = 128
	x = []
	c = 1
	for s in ls:
		x.append(amount)
		amount = amount + 128
	return x

def plot_line_graph(m_y, m_x, subplot, ylabel, xlabel, leg, i, titl, colr):
	index = np.arange(len(m_y))
	plt.subplot(subplot)
	plt.plot(m_x, m_y, label=leg, color=colr)
	plt.ylabel(ylabel)
	plt.xlabel(xlabel)
	plt.grid(True)
	plt.xticks(m_x)
	plt.gca().yaxis.set_minor_formatter(NullFormatter())
	if i == 2:
		plt.subplots_adjust(top=0.96, bottom=0.05, left=0.05, right=0.9, hspace=0.25,
                    wspace=0.35)
	else:
		plt.subplots_adjust(top=0.96, bottom=0.05, left=0.05, right=0.9, hspace=0.25,
                    wspace=0.35)
	#for i in range(0, len(m_y)):
	#	plt.text(m_x[i], m_y[i], round(m_y[i], 2), fontsize=10)
	plt.title(titl)
	plt.legend(loc=1, bbox_to_anchor=(1.12, 1.0)) #1.28, 1.0

def save_plot(path_n_file):
	path = get_path(extention="z_graphs/")
	#print path
	plt.savefig(str(path)+str(path_n_file)+".png", dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None)

def create_time_lines(time_stamps, path, ylabl, title, subplot, txts):
	i = 0
	for ls_y in time_stamps:
		ls_x = calc_x_axis(ls_y)
		#print ls_y
		#print ls_x
		plot_line_graph(ls_y, ls_x, subplot, ylabl, "Objects in second with "+title[0], 
			architecture[i], i, 'Step-wise '+txts+' load increase in '+title[0]+' scenario.', 
			clr[i])
		i = i + 1

def plot_graphs(means=[], time_stamps=[], fig_nr=1, name="", subplot=221):
	plt.figure(fig_nr)
	plt.subplots(1,1, figsize=(30, 14), facecolor='w', edgecolor='k')
	create_time_lines(means[0], name+"cpu", "CPU ussage in %", ["Read and Update mix"], subplot, "CPU")
	create_time_lines(means[1], name+"disk", "Disk reads in mb/s", ["Read and Update mix"], subplot+1, "Disk Read")
	create_time_lines(time_stamps[0], name+"-cpu-time", "Time in sec", ["Read and Update mix"], subplot+2, "CPU")
	create_time_lines(time_stamps[1], name+"-cpu-time", "Time in sec", ["Read and Update mix"], subplot+3, "Disk Read")
	save_plot(name+"cpu-and-disk-read")

def handle_files(path_an_min, t):
	#mean_values, time_stamp_values = cross_validation_data(path_an_min)
	#print mean_values
	#print time_stamp_values
	if t == 2:
		#plot_graphs(means=mean_values, time_stamps=time_stamp_values, name=path_an_min[0])
		pass
	elif t == 1:
		means_val = read_cross_data(get_path(extention="x_result/"), find_csv_filenames(ext="x_result/", suffix=path_an_min[0]))
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
		handle_files(path_n_min, 1)
	elif path_n_min[1] == 2:
		handle_files(path_n_min, 2)
	else:
		print 'Wrong option typ -h for help.'

""" Start. """
if __name__ == "__main__":
	main(sys.argv[1:3])