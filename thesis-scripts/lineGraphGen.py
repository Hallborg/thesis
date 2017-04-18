#!/usr/bin/env python2
import numpy as np
import csv
import matplotlib.pyplot as plt
import sys
import os
import itertools
from os import listdir
from matplotlib.ticker import NullFormatter
global PEAK_SIZE
global DEVICE_INDEX


""" Global variables """
MIN_SIZE_AT_RECIVE = 100 # 100 och 5
CSV_AMOUNT=0
PEAK_SIZE = 15
DEVICE_INDEX = 0

lb1 = ['BM', 'Docker', 'LXC', 'DockerIso']
clr = ['g', 'b', 'orange', 'r']
device=['cpu', 'sent', 'recive']
lb_operation=['write', 'read', 'update', 'delete']

""" Collects path to the files and all file names. """
def get_path(extention):
	f = []
	real_path = str(os.path.dirname(os.path.realpath(__file__)))\
	+"/../csv-and-graphs/%s" %(extention)
	for (path, dirnames, filenames) in os.walk(real_path):
		f.append(path)
		for file in filenames:
			if ".DS_Store" in file: pass
			else:
				f.append(file)
		#f.extend(filenames)
		#print filenames
	set_global_var(len(f))
	if 'cpu' in extention:
		set_global_var3(0)
	elif 'sent' in extention:
		set_global_var3(1)
	elif 'recive' in extention:
		set_global_var3(2)
	return f

""" Sets the global variables to the amount of files and min. """
def set_global_var(value):
	global CSV_AMOUNT
	CSV_AMOUNT = value
def set_global_var2(value):
	global MIN_SIZE_AT_RECIVE
	MIN_SIZE_AT_RECIVE = value
def set_global_var3(value):
	global DEVICE_INDEX
	DEVICE_INDEX = value

""" Reads all files and appends the content to a list. """
def csv_to_bar_list(path_n_min_list):
	mean_for_bar_graph = []
	path = get_path("csv/"+path_n_min_list[0]+"/") #"csv/write-read/"
	set_global_var2(path_n_min_list[1])
	row_amounts = []
	labelSt = []
	for i in range(1,CSV_AMOUNT):
		with open(str(path[0])+str(path[i]), 'r') as f:
			print str(path[i])
			means, row_am = bar_graph_calc(csv.reader(f), str(path[i]), i-1)
			mean_for_bar_graph.append(means)
			row_amounts.append(row_am)
			if 'bm-dockeriso' in path[i]:
				labelSt.append(3)
			elif 'bm-docker' in path[i]:
				labelSt.append(1)
			elif 'bm-lxc' in path[i]:
				labelSt.append(2)
			else:
				labelSt.append(0)
	return mean_for_bar_graph, row_amounts, labelSt

""" Filter a list of entries to where cluster starts to 
	recive data, and creates a list of mean values for those. """
def bar_graph_calc(reader, name, k):
	max_time = 45
	mean_of_nodes = []
	mean_over_time = []
	reader = list(reader)
	reader = reader[3:]
	row_amount = [0]*5
	i = 0
	j = 0
	time_count = 0
	real_time = 0
	data_to_anova= []
	for row in reader:
		row2 = reader[i+1]
		#print row2[1:]
		s2 = mean_calc(row2[1:])
		s = mean_calc(row[1:])
		if float(s) > float(MIN_SIZE_AT_RECIVE):
			real_time = real_time + 1
			if int(time_count) < int(max_time):
				mean_of_nodes.append(mean_calc(row[1:]))
				row_amount[j] = row_amount[j] + 1
				time_count = time_count + 1
			if float(s2) < float(MIN_SIZE_AT_RECIVE):
				mean_over_time.append(mean_calc(mean_of_nodes))
				data_to_anova.append(mean_of_nodes)
				print "Time on graph: %d 		: 		Time it actually took: %d" % (time_count, real_time)
				#print mean_of_nodes
				time_count = 0
				real_time = 0
				mean_of_nodes = []
				j = j + 1
		if i < len(reader)-2: 
			i = i+1
	mean_over_time.pop(1)
	row_amount.pop(1)
	data_to_anova.pop(1)
	j = 0
	for a_list in data_to_anova:
		print len(a_list)
		write_csv_to_a_file(a_list, j, lb1[k], device[DEVICE_INDEX])
		j = j + 1
	return mean_over_time, row_amount

""" Calculates mean value of a list. """
def mean_calc(a_list):
	a_sum = 0.0
	for entry in a_list:
		a_sum = a_sum+float(entry)
	a_sum = a_sum/len(a_list)
	return a_sum

""" Appends bars from every file to the graph. """
def create_figs(means, lb, clr, index, width, ax, i, delay, men_std):
	#men_std = (1000, 1000, 1000, 1000)
	opacity = 0.65
	error_config = {'ecolor': '0.4'}
	rects = ax.bar(index-delay, means, width, 
		alpha=opacity, color=clr, yerr=men_std,
		error_kw=error_config, label =lb)

	for rect in rects:
		height = rect.get_height()
		plt.text(rect.get_x() + rect.get_width()/2., 1.05*height,
			'%d' % int(height), ha='left', va='bottom')
	return delay

""" Configures the graph, plots the bars and displays the figure. """
def create_bar_graph(means, graph_type, m_std, lb, xlabel, ylabel, title, xtick, labelIndex):
	index = np.arange(len(means[0]))
	#print index
	width = 0.15
	i = 0
	fig, ax = plt.subplots(1,1, figsize=(18, 6), facecolor='w', edgecolor='k') # 
	fig.subplots_adjust(hspace = .5, wspace=.001)
	delay = 0
	for m in means:
		delay = create_figs(m, lb[labelIndex[i]], clr[labelIndex[i]], index, width, ax, i, delay, m_std[i])
		i=i+1
		delay = delay-width
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.title(title)
	if len(means) == 2:
		placement = index + width/2
	else:
		placement = index + width + width/2
	plt.xticks(placement, xtick)
	plt.legend(loc=1, bbox_to_anchor=(1.1, 1.0))
	path = get_path("graphs/")
	plt.savefig(path[0]+graph_type+".png", dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None)
	#plt.show()

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
			argv[1] = float(argv[1])
		except ValueError as e:
			print "Usage: ./lineGraphGen.py <extend the directory(cpu, write-read, memory)>\
		 <Integer (min value where something happens)> <Integer (1 bars, 2 line)>"
			exit()
		else:
			try:
				argv[2] = int(argv[2])
			except ValueError as e:
				print "Usage: ./lineGraphGen.py <extend the directory(cpu, write-read, memory)>\
		 		<Integer (min value where something happens)> <Integer (1 bars, 2 line)>"
				exit()
			else:
				return [argv[0], argv[1]], argv[2]

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

""" Delete trunking phase! """
def del_one(m):
	for s in m:
		if len(s) > 3:
			del s[2]
		if len(s) > 3:
			del s[3]
	return m

"""  """
def csv_to_line_list(path_n_min):
	means_for_line_graph = []
	time_stamps = []
	path = get_path("csv/"+path_n_min[0]+"/") #"csv/write-read/"
	set_global_var2(path_n_min[1])
	row_amounts = []
	labelSt = []
	for i in range(1,CSV_AMOUNT): # CSV_AMOUNT
		with open(str(path[0])+str(path[i]), 'r') as f:
			print "Current file %s is in use." % (str(path[i]))
			temp1, temp2 = filter_the_file(csv.reader(f), path[i])
			means_for_line_graph.append(temp1)
			time_stamps.append(temp2)
			if 'bm_dockeriso' in path[i]:
				labelSt.append(3)
			elif 'bm_docker' in path[i]:
				labelSt.append(1)
			elif 'bm_lxc' in path[i]:
				labelSt.append(2)
			else:
				labelSt.append(0)
	return means_for_line_graph, labelSt, time_stamps

"""  """
def filter_the_file(reader, name):
	i = 0
	loop = True
	if '_bm_bm' in name:
		limit = MIN_SIZE_AT_RECIVE-1.0
	else:
		limit = MIN_SIZE_AT_RECIVE
	zeros = 0
	sk = 0
	count = 0
	graphs = 0
	the_list = list(reader)[3:]
	list_to_ret = []
	temp_list = []
	timestamps_of_peaks = []
	time_track = 0
	while loop:
		entry = the_list[i]
		ent = entry[1:]
		sum_of = mean_calc(ent)
		if (float(sum_of) > float(limit)):
			temp_list.append(ent)
			time_track = time_track + 1
			limit = limit + 0.15
			sk = sk + 1
			zeros = 0
			count = 0
		else:
			temp_list.append([0,0,0])
			zeros = zeros + 1
			count = count + 1
			#graphs = 0
		if count >= 20:
			list_to_ret.append('Walla')
			if '_bm_bm' in name:
				limit = MIN_SIZE_AT_RECIVE-1.0
			else:
				limit = MIN_SIZE_AT_RECIVE
		if (sk >= 1) & (zeros >= 4) & (count < 20):
			#print temp_list
			tmp = best_values(temp_list)
			t = mean_calc(tmp)
			list_to_ret.append(t)
			timestamps_of_peaks.append(time_track)
			temp_list = []
			sk = 0
			zeros = 0
			count = 0
			time_track = 0
		i = i +1
		if i >= len(the_list)-1:
			loop = False
	spl = [list(y) for x, y in itertools.groupby(list_to_ret, lambda z: z == 'Walla') if not x]
	peak_timestamps = [timestamps_of_peaks[i:i + PEAK_SIZE] for i in xrange(0, len(timestamps_of_peaks), PEAK_SIZE)]
	spl = filter_on_amount(spl)
	peak_timestamps = filter_on_amount(peak_timestamps)
	i = 0
	print spl
	for ins in spl:
	 	print 'Graph %d had: %d peaks.' % (i+1, len(ins))
	 	i = i + 1
	print '\n'
	return spl, peak_timestamps

"""  """
def best_values(l):
	val = l[0]
	best1 = val[0]
	best2 = val[1]
	best3 = val[2]
	for i in range(1, len(l)):
		#print i
		val = l[i]
		#print val
		if float(best1) < float(val[0]):
			#print 'Previous: %f , Replecement: %f' % (float(best1), float(val[0]))
			best1 = val[0]
		if float(best2) < float(val[1]):
			#print 'Second'
			best2 = val[1]
		if float(best3) < float(val[2]):
			#print 'Third'
			best3 = val[2]
	#print best1, best2, best3
	return [best1, best2, best3]

"""  """
def filter_on_amount(spl):
	list_ret = []
	for ins in spl:
		if len(ins) == PEAK_SIZE:
			list_ret.append(ins)
		elif len(ins) > PEAK_SIZE:
			good = ins[:len(ins)/2]
			am_to_rm = len(ins) - PEAK_SIZE
			temp = ins[len(ins)/2:]
			del_index = [0]*am_to_rm
			for j in range(0, len(del_index)):
				for i in range(1, len(temp)):
					to_del = temp[i-1]
					if to_del > temp[i]:
						to_del = temp[i]
						del_index[j] = i
				del temp[del_index[j]]
			list_ret.append(good+temp)
		elif len(ins) < PEAK_SIZE:
			if len(ins) > 5:
				list_ret.append(ins)
	return list_ret

"""  """
def calc_x_axis(ls):
	amount = 128
	x = []
	for s in ls:
		temp = []
		for i in range(0, len(s)):
			temp.append(amount)
			amount = amount + 128
		amount = 128
		x.append(temp)
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
	plt.legend(loc=1, bbox_to_anchor=(1.28, 1.0))

def save_plot(path_n_file):
	path = get_path("graphs/")
	plt.savefig(path[0]+path_n_file+".png", dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None)

""" Handle and Create the bar graphs. """
def handle_n_create_bars(path_n_min):
	m, rows, labelIndex = csv_to_bar_list(path_n_min)
	print rows
	print m
	#m = del_one(m)
	#rows = del_one(rows)
	m_std = calc_mean_std(m)
	rows_std = calc_mean_std(rows)
	print rows
	print m
	if 'recive' in path_n_min[0] or 'sent' in path_n_min[0]:
		create_bar_graph(m, path_n_min[0], m_std, lb1, 'I/O operation', 'kb/s', 
			'I/O intensive write/read/update/delete load in kb/s', ('Write', 'Read', 'Update', 'Delete'), labelIndex)
	elif 'cpu' in path_n_min[0]:
		create_bar_graph(m, path_n_min[0]+"-bar-cpu-usage", m_std, lb1, 'Operation', 'percent (%)', 
			'CPU intensive write/read/update/delete load in percent', ('Write', 'Read', 'Update', 'Delete'), labelIndex)
		create_bar_graph(rows, path_n_min[0]+'-bar-time-it-took', rows_std, lb1, 'Operation', 'Time in sec', 
			'CPU intensive write/read/update/delete load in sec', ('Write', 'Read', 'Update', 'Delete'), labelIndex)
	operands = '-'+device[0]+'-'+lb_operation[0]+'.csv'
	#fix_files(operands)
	#elif 'memory' in path_n_min[0]:
	#	create_bar_graph(m, path_n_min[0], m_std, lb1, 'Operation', 'usage in kb', 
	#		'Memory intensive write/read/mix load in kb', ('Write', 'Read', 'Mix'))
	#	create_bar_graph(rows, path_n_min[0]+'-2', rows_std, lb1, 'Operation', 'Time in sec', 
	#		'Memory intensive write/read/mix load in sec', ('Write', 'Read', 'Mix'))

def create_time_lines(time_stamps, path, ylabl, title, lblIndex, fig_nr):
	plt.figure(fig_nr)
	plt.subplots(1,1, figsize=(18, 11), facecolor='w', edgecolor='k')
	j = 0
	for ls_y in time_stamps:
		ls_x = calc_x_axis(ls_y)
		i = 0
		subplot = 221
		for ins in ls_y:
			plot_line_graph(ins, ls_x[i], subplot, ylabl, "Objects in second with "+title[i], 
				lb1[lblIndex[j]]+'-'+title[i], i, 'Step-wise load increase in '+title[i]+' scenario.', 
				clr[lblIndex[j]])
			i = i + 1
			subplot = subplot + 1
		j = j + 1
	save_plot(path)

""" Handle and create Line graphs. """
def handle_n_create_lines(path_n_min):
	title = ['Write', 'Read', 'Update', 'Delete']
	means, lblIndex, time_stamps = csv_to_line_list(path_n_min)

	create_time_lines(means, path_n_min[0], "CPU ussage in %", title, lblIndex, 1)
	create_time_lines(time_stamps, path_n_min[0]+"-time", "Time in sec", title, lblIndex, 2)
	
def write_csv_to_a_file(a_list, i, name, device_name):
	dir_path = os.path.dirname(os.path.realpath(__file__))
	file = open("%s/../csv-and-graphs/anova/csv/%s-%s-%s.csv" % (str(dir_path), name, device_name, lb_operation[i]), "w")
	#file.write(a_list)
	for item in a_list:
		file.write(str(item)+', ')
	file.close()

""" Main window. """
def main(argv):
	path_n_min, type_of = handle_argvs(argv)
	if type_of == 1:
		handle_n_create_bars(path_n_min)
	elif type_of == 2:
		handle_n_create_lines(path_n_min)
	else:
		print 'Wrong option typ -h for help.'



""" Start. """
if __name__ == "__main__":
	main(sys.argv[1:4])


