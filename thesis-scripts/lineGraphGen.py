#!/usr/bin/env python2
import numpy as np
import csv
import matplotlib.pyplot as plt
import sys
import os
global MIN_SIZE_AT_RECIVE

""" Global variables """
MIN_SIZE_AT_RECIVE = 100 # 100 och 5
CSV_AMOUNT=0

""" Collects path to the files and all file names. """
def get_path():
	f = []
	real_path = str(os.path.dirname(os.path.realpath(__file__)))\
	+"/../csv-and-graphs/csv/write-read/"
	for (path, dirnames, filenames) in os.walk(real_path):
		f.append(path)
		f.extend(filenames)
		#print filenames
	set_global_var(len(f))
	return f

""" Sets the global variable to the amount of files. """
def set_global_var(value):
	global CSV_AMOUNT
	CSV_AMOUNT = value

""" Reads all files and appends the content to a list. """
def csv_to_bar_list():
	mean_for_bar_graph = []
	path = get_path()
	for i in range(1,CSV_AMOUNT):
		with open(str(path[0])+str(path[i]), 'r') as f:
			mean_for_bar_graph.append(bar_graph_calc(csv.reader(f)))
	return mean_for_bar_graph

""" Filter a list of entries to where cluster starts to 
	recive data, and creates a list of mean values for those. """
def bar_graph_calc(reader):
	mean_of_nodes = []
	mean_over_time = []
	reader = list(reader)
	reader = reader[1:]
	i = 0
	for row in reader:
		row2 = reader[i+1]
		if float(row[1]) > MIN_SIZE_AT_RECIVE:
			mean_of_nodes.append(mean_calc(row[1:]))
			if float(row2[1]) < MIN_SIZE_AT_RECIVE:
				mean_over_time.append(mean_calc(mean_of_nodes))
				mean_of_nodes = []
		if i < len(reader)-2: i = i+1
	return mean_over_time

""" Calculates mean value of a list. """
def mean_calc(a_list):
	a_sum = 0.0
	for entry in a_list:
		a_sum = a_sum+float(entry)
	a_sum = a_sum/len(a_list)
	return a_sum

""" Appends bars from every file to the graph. """
def create_figs(means, lb, clr, index, width, ax, i, delay):
	men_std = (1000, 1000, 1000)
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
def create_graph(means):
	lb = ['BM', 'Docker', 'LXC', 'DockerIso']
	clr = ['g', 'b', 'orange', 'r']
	index = np.arange(len(means[0]))
	width = 0.15
	i = 0
	fig, ax = plt.subplots(1,1, figsize=(18, 6), facecolor='w', edgecolor='k') # 
	fig.subplots_adjust(hspace = .5, wspace=.001)
	rect = []
	delay = 0
	for m in means:
		delay = create_figs(m, lb[i], clr[i], index, width, ax, i, delay)
		i=i+1
		delay = delay-width
	plt.xlabel('I/O operation')
	plt.ylabel('kb/s')
	plt.title('I/O intensive write/read/mix load in kb/s')
	plt.xticks(index + width + width/2, ('Write', 'Read', 'Mix'))
	plt.legend(loc=1, bbox_to_anchor=(1.1, 1.0))
	plt.show()

""" Main window. """
def __main__():
	m = csv_to_bar_list()
	#print m
	create_graph(m)



""" Start. """
__main__()
