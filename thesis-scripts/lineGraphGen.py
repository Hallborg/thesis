#!/usr/bin/env python2
import numpy as np
import csv
import matplotlib.pyplot as plt
import sys
import os
import itertools
#global MIN_SIZE_AT_RECIVE
global PEAK_SIZE


""" Global variables """
MIN_SIZE_AT_RECIVE = 100 # 100 och 5
CSV_AMOUNT=0
PEAK_SIZE = 15

lb1 = ['BM', 'Docker', 'LXC', 'DockerIso']

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
	return f

""" Sets the global variables to the amount of files and min. """
def set_global_var(value):
	global CSV_AMOUNT
	CSV_AMOUNT = value
def set_global_var2(value):
	global MIN_SIZE_AT_RECIVE
	MIN_SIZE_AT_RECIVE = value

""" Reads all files and appends the content to a list. """
def csv_to_bar_list(path_n_min_list):
	mean_for_bar_graph = []
	path = get_path("csv/"+path_n_min_list[0]+"/") #"csv/write-read/"
	set_global_var2(path_n_min_list[1])
	row_amounts = []
	for i in range(1,CSV_AMOUNT):
		with open(str(path[0])+str(path[i]), 'r') as f:
			means, row_am = bar_graph_calc(csv.reader(f))
			mean_for_bar_graph.append(means)
			row_amounts.append(row_am)
	return mean_for_bar_graph, row_amounts

""" Filter a list of entries to where cluster starts to 
	recive data, and creates a list of mean values for those. """
def bar_graph_calc(reader):
	mean_of_nodes = []
	mean_over_time = []
	reader = list(reader)
	reader = reader[1:]
	row_amount = [0, 0, 0, 0]
	i = 0
	j = 0
	for row in reader:
		row2 = reader[i+1]
		if float(row[1]) > float(MIN_SIZE_AT_RECIVE):
			mean_of_nodes.append(mean_calc(row[1:]))
			row_amount[j] = row_amount[j] + 1
			if float(row2[1]) < float(MIN_SIZE_AT_RECIVE):
				mean_over_time.append(mean_calc(mean_of_nodes))
				mean_of_nodes = []
				j = j + 1
		if i < len(reader)-2: i = i+1
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
	opacity = 0.4
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
def create_bar_graph(means, graph_type, m_std, lb, xlabel, ylabel, title, xtick):
	clr = ['g', 'b', 'orange', 'r', 'y']
	index = np.arange(len(means[0]))
	#print index
	width = 0.15
	i = 0
	fig, ax = plt.subplots(1,1, figsize=(18, 6), facecolor='w', edgecolor='k') # 
	fig.subplots_adjust(hspace = .5, wspace=.001)
	delay = 0
	for m in means:
		delay = create_figs(m, lb[i], clr[i], index, width, ax, i, delay, m_std[i])
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
			argv[1] = int(argv[1])
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
		if len(s) == 4:
			del s[2]
	return m

"""  """
def csv_to_line_list(path_n_min):
	means_for_line_graph = []
	path = get_path("csv/"+path_n_min[0]+"/") #"csv/write-read/"
	set_global_var2(path_n_min[1])
	row_amounts = []
	for i in range(1,2): # CSV_AMOUNT
		with open(str(path[0])+str(path[i]), 'r') as f:
			means_for_line_graph.append(filter_the_file2(csv.reader(f)))
	return means_for_line_graph

def check_biggest(val1, val2, val3):
	best = float(val1)
	if float(val2) > best:
		best = float(val2)
	if float(val3) > best:
		best = float(val3)
	return best

"""  """
def filter_the_file(reader):
	i = 0
	loop = True
	prev = -1
	nextt = 1
	the_list = list(reader)[2:]
	list_to_ret = []
	graph_delimiter_count = 0
	while loop:
		if prev > -1:
			prev_en = the_list[prev]
		else:
			prev_entry = the_list[i]
			#list_to_ret.append(0)
		next_entry = the_list[nextt]
		entry = the_list[i]

		if (float(entry[1]) > 2.0) | (float(entry[2]) > 2.0) | (float(entry[3]) > 2.0):
			best_node1 = check_biggest(prev_entry[1], entry[1], next_entry[1])
			best_node2 = check_biggest(prev_entry[2], entry[2], next_entry[2])
			best_node3 = check_biggest(prev_entry[3], entry[3], next_entry[3])

			node_mean = mean_calc([best_node1, best_node2, best_node3])
			i = nextt + 2
			nextt = i + 1
			prev = i - 1
			graph_delimiter_count = 0
			list_to_ret.append(node_mean)
			#print node_mean
		else:
			i = i + 1
			nextt = nextt + 1
			prev = prev + 1
			graph_delimiter_count = graph_delimiter_count + 1
		if graph_delimiter_count >= 5:
			list_to_ret.append(0)
		if nextt >= len(the_list):
			loop = False

	return list_to_ret


def filter_the_file2(reader):
	i = 0
	loop = True
	limit = 10.0
	prev = -1
	nextt = 1
	zeros = 0
	follower = 0
	sk = 0
	sk2 = 0
	count = 0
	g = 22
	graph_limit = g
	the_list = list(reader)[2:]
	list_to_ret = []
	graph_delimiter_count = 0
	temp_list = []
	while loop:
		entry = the_list[i]
		ent = entry[1:]
		sum_of = float(ent[0]) + float(ent[1]) + float(ent[2])
		if (sum_of > limit):
			#print sum_of
			temp_list.append(ent)
			sk = sk + 1
			sk2 = 0
			zeros = 0
			#limit = limit + 0.05
			graph_limit = graph_limit + 1
		else:
			sk2 = sk2 + 1
			temp_list.append([0, 0, 0])
			zeros = zeros + 1
			#print graph_limit, zeros
			graph_limit = g
			#print zeros
			if zeros >= graph_limit:
				#print follower
				if not list_to_ret:
					list_to_ret.append('Walla')
					follower = follower + 1
					zeros = 0
				elif isinstance(list_to_ret[follower-1], float):
					list_to_ret.append('Walla')
					follower = follower + 1
					print 'Limit reached at: %d %%' % (limit)
					limit = 9.0
					zeros = 0
					graph_limit = g
		if (sk >= 1) & (sk2 >= 1):
			t = 0.0
			tmp = best_values(temp_list)
			t = mean_calc(tmp)
			list_to_ret.append(t)
			follower = follower + 1
			#print temp_list
			temp_list = []
			count = count + 1
			#zeros = 0
			#graph_limit = 21
			sk = 0
			sk2 = 0
		i = i +1
		prev = prev + 1
		if i >= len(the_list)-1:
			loop = False
	#print len(list_to_ret)
	spl = [list(y) for x, y in itertools.groupby(list_to_ret, lambda z: z == 'Walla') if not x]
	i = 0
	print 'Lenght of peaks with trunks: %d.' % (len(spl))
	for ins in spl:
		if len(ins) < 10:
			del spl[i]
		i = i + 1
	spl = filter_on_amount(spl)
	i = 0
	for ins in spl:
		#print ins
	 	print 'Graph %d had: %d peaks.' % (i+1, len(ins))
	 	#print ins
	 	i = i + 1
	return spl

"""  """
def best_values(l):
	val = l[0]
	best1 = val[0]
	best2 = val[1]
	best3 = val[2]
	#print l
	for i in range(1, len(l)):
		#print i
		val = l[i]
		#print val
		if float(best1) < float(val[0]):
			print 'Previous: %f , Replecement: %f' % (float(best1), float(val[0]))
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
		if len(ins) > PEAK_SIZE:
			good = ins[:len(ins)/2]
			#print good, len(good)
			am_to_rm = len(ins) - PEAK_SIZE
			print am_to_rm
			temp = ins[len(ins)/2:]
			#print temp, len(temp)
			del_index = [0]*am_to_rm
			for j in range(0, len(del_index)):
				for i in range(1, len(temp)):
					to_del = temp[i-1]
					if to_del > temp[i]:
						to_del = temp[i]
						del_index[j] = i
				del temp[del_index[j]]
			#print del_index
			list_ret.append(good+temp)
	#print list_ret
	return list_ret

"""  """
def calc_x_axis(ls):
	amount = 32
	x = []
	for s in ls:
		temp = []
		for i in range(0, len(s)):
			temp.append(amount)
			amount = amount + 32
		amount = 32
		x.append(temp)
	return x

def plot_line_graph(m_y, m_x, ylabel):
	plt.plot(m_x, m_y)
	plt.ylabel(ylabel)

def save_plot(path_n_file):
	path = get_path("graphs/")
	plt.savefig(path[0]+path_n_file+".png", dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None)

""" Handle and Create the bar graphs. """
def handle_n_create_bars(path_n_min):
	m, rows = csv_to_bar_list(path_n_min)
	m = del_one(m)
	rows = del_one(rows)
	m_std = calc_mean_std(m)
	rows_std = calc_mean_std(rows)
	print rows
	print m
	if 'write-read' in path_n_min[0]:
		create_bar_graph(m, path_n_min[0], m_std, lb1, 'I/O operation', 'kb/s', 
			'I/O intensive write/read/mix load in kb/s', ('Write', 'Read', 'Mix'))
	elif 'cpu' in path_n_min[0]:
		create_bar_graph(m, path_n_min[0], m_std, lb1, 'Operation', 'percent (%)', 
			'CPU intensive write/read/mix load in percent', ('Write', 'Read', 'Mix'))
		create_bar_graph(rows, path_n_min[0]+'-2', rows_std, lb1, 'Operation', 'Time in sec', 
			'CPU intensive write/read/mix load in sec', ('Write', 'Read', 'Mix'))
	#elif 'memory' in path_n_min[0]:
	#	create_bar_graph(m, path_n_min[0], m_std, lb1, 'Operation', 'usage in kb', 
	#		'Memory intensive write/read/mix load in kb', ('Write', 'Read', 'Mix'))
	#	create_bar_graph(rows, path_n_min[0]+'-2', rows_std, lb1, 'Operation', 'Time in sec', 
	#		'Memory intensive write/read/mix load in sec', ('Write', 'Read', 'Mix'))

""" Handle and create Line graphs. """
def handle_n_create_lines(path_n_min):
	print 'Fun Fun Fun at %s !' % (path_n_min[0])
	means = csv_to_line_list(path_n_min)
	ls_y = means[0]
	ls_x = calc_x_axis(ls_y)
	#print ls
	#m = filter_means(means[0])
	#print len(m)
	#print m
	#m = means[0]
	print ls_x
	i = 0
	for ins in ls_y:
		#plot_line_graph(ins, "CPU ussage in %")
		plot_line_graph(ins, ls_x[i], "CPU ussage in %")
		i = i + 1
	save_plot(path_n_min[0])

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


