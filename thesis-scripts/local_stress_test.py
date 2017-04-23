#!/usr/bin/env python2
from cassandra.cluster import Cluster
import os
import sys
import subprocess
import time

tables = ["edr_by_id","edr_by_date","edr_by_service","edr_by_destination","edr_by_date2", "edr_by_id2"]
#new_tables = ["edr_by_id3","edr_by_date3","edr_by_service3","edr_by_destination3","edr_by_date4", "edr_by_id4"]
#columns = ["id", "service", "created_at", "started_at", "service_units", "event_charges", "call_event", "data_event", "destination"]

column_str = "id, service, created_at, started_at, service_units, event_charges, call_event, data_event"
column_str2 = "id, destination, service, created_at, started_at, service_units, event_charges, call_event, data_event"

def table_to_file():
	i = 0
	for t in tables:
		cols = column_str
		if 'edr_by_destination' in t: cols = column_str2
		copy_table_to_file = "-e \"COPY cdr.%s ( %s ) TO '../temps/temp-table%d.csv'\"" % (t, cols, i)
		bash_command = "cqlsh localhost 9042 %s;" % (copy_table_to_file)
		output = subprocess.check_output(['bash','-c', bash_command])
		print bash_command
		print output
		i = i + 1

def file_to_table():
	i = 0
	for t in tables:
		cols = column_str
		if 'edr_by_destination' in t: cols = column_str2
		create_table_from_file = "-e \"COPY cdr.%s ( %s ) FROM '../temps/temp-table%d.csv'\"" % (t, cols, i)
		bash_command = "cqlsh localhost 9042 %s;" % (create_table_from_file)
		output = subprocess.check_output(['bash','-c', bash_command])
		print bash_command
		print output
		i = i + 1

def local_read(max_time):
	t0 = time.clock()
	t1 = (time.clock() - t0)
	print t1
	while t1 < max_time:
		#print "Time is: %s" % (t1)
		t1 = (time.clock() - t0)

def fix_some_data():
	cluster = Cluster()
	session = cluster.connect()
	session.execute('USE cdr')
	data = []
	for i in range(0, 4):
		with open('../dataModel/mockdata-%d' % (i), 'r') as f:
			for line in f:
				l = line
				data.append(str(l).replace('\n',''))
		for ent in data:
			if i == 3: s = i + 1
			else: s = i
			print "INSERT INTO cdr.%s JSON '%s'" % (tables[s],ent)
			session.execute("INSERT INTO cdr.%s JSON '%s'" % (tables[s],ent))

def drop_and_rm():
	bash_command = "cqlsh localhost 9042 -e \"DROP KEYSPACE cdr \""
	output = subprocess.check_output(['bash','-c', bash_command])
	bash_command = "rm -rf /var/lib/cassandra/cdr/*;"
	output = subprocess.check_output(['bash','-c', bash_command])
	bash_command = "cqlsh localhost 9042 -e \"source '../cassandra-models/edr.cql'\";"
	output = subprocess.check_output(['bash','-c', bash_command])

def main(argv):
	if int(argv[0]) == 0:
		fix_some_data()
	elif int(argv[0]) == 1:
		table_to_file()
	elif int(argv[0]) == 2:
		file_to_table()
	elif int(argv[0]) == 3:
		drop_and_rm()
	elif int(argv[0]) == 4:
		local_read(float(argv[1]))

if __name__ == "__main__":
	main(sys.argv[1:3])