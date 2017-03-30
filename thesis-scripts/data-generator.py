#!/usr/bin/env python2
import datetime
import time
import random
import sys
import subprocess
import os

""" Amount of entries we create! """
service_to_use = 0

""" Defines enums that exist in the database. """
unit_of_measure_enum=["seconds", "monetary", "bytes"]
resource_type_enum=["Money", "Kilobytes", "Seconds", "Units"]
charged_type_enum=["REAL", "BONUS", "PARTITION"]
traffic_case_enum=["originating", "terminating", "forwarding"]
event_type_enum=["Voice", "sms", "mms", "video"]
edr_service_enum=["1", "2"]
products_enum=["Call Plan Normal", "Call Plan Low", "Call Plan High", "Call Plan Allin", \
"Data Plan Normal", "Data Plan Low", "Data Plan High"]
access_point_name_enum=["example.com", "hallborg.se", "patryk.se", "wikipedia.org", \
"amazon.com", "instagram.com", "twitter.com", "github.com", "reddit.com"]
roming_enum=["false", "true"]

""" Make sure that passed argument is an integer """
def arg_t(argv):
	try:
		argv[0] = int(argv[0])
	except ValueError:
		print "Usage ./data-generator.py <Integer>"
		exit()
	else:
		if argv[0] < 0:
			print "Usage ./data-generator.py <Integer>\nNo negatives!"
			exit()
		elif argv[0] > 5100000:
			print "Usage ./data-generator.py <Integer>\nNumber is too big! \
			5.000.000 is enough."
			exit()
		amt = argv[0]
		return amt

""" Service-unit defined """
def create_service_unit():
	serv_unit_ammount = random.randint(46, 50000)
	if service_to_use == 2:
		serv_unit_unit = unit_of_measure_enum[2]
	else:
		serv_unit_unit = unit_of_measure_enum[random.randint(0, 1)]
	service_unit = """\
"service_units" : {"amount": %d, "unit_of_measure": "%s"}\
""" % (serv_unit_ammount, serv_unit_unit)
	return service_unit

""" Product type defined """
def create_product():
	if service_to_use == 2:
		rand_product = random.randint(4, 6)
	else:
		rand_product = random.randint(0, 3)
	prod_id = str(rand_product)
	prod_name = products_enum[rand_product]
	products= """\
"products" : { "id": "%s", "name": "%s" } \
""" % (prod_id, prod_name)
	return products

""" Defines charged units """
def create_charged_units(service_unit):
	charged_units = service_unit.replace("service", "charged")
	return charged_units

""" Charge ammounts list handling """
def create_charged_amounts():
	nr_of_charged_am = random.randint(1, 9)
	charged_amounts_list = []
	for i in range(0, nr_of_charged_am):
		charged_amounts_amount = random.randint(50, 350)
		charged_amounts_id = str(gen_hex_code(5))
		charged_amounts_endbalance = random.uniform(0.0, 2100.0)
		charged_amounts_res_type = resource_type_enum[random.randint(0,3)]
		charged_amounts_name = charged_type_enum[random.randint(0,2)]
		charged_amounts_exp_date = "null"
		charged_amounts_charg_type = charged_type_enum[random.randint(0,2)]
		if service_to_use == 2:
			charged_amounts_event_type = "Data"
		else:
			charged_amounts_event_type = event_type_enum[random.randint(0,3)]
		charged_amounts_i = """\
{ "amount": %d, \
"id": "%s", \
"end_balance": %.2f, \
"resource_type": "%s", \
"name": "%s", \
"expiry_date": %s, \
"charged_type": "%s", \
"event_type": "%s" }\
""" % (charged_amounts_amount, charged_amounts_id, charged_amounts_endbalance,\
			charged_amounts_res_type, charged_amounts_name, charged_amounts_exp_date, \
			charged_amounts_charg_type, charged_amounts_event_type)
		charged_amounts_list.append(charged_amounts_i)
	charged_amounts = """\
"charged_amounts": %s\
""" % (charged_amounts_list)
	charged_amounts = charged_amounts.replace("\'", "")
	return charged_amounts

""" Event charges """
def create_event_charges(service_unit_t):
	charged_amounts = create_charged_amounts()
	products = create_product()
	charged_units = create_charged_units(service_unit_t)
	event_charges = """\
"event_charges": { %s, %s, %s }\
""" % (charged_amounts, products, charged_units)
	return event_charges

""" A location generator """
def create_a_location():
	alocation_destination = "732103"+gen_hex_code(8) # 6 first do not change
	alocation = """ "a_party_location": { "destination": "%s"} """ % (alocation_destination)
	return alocation

""" B location generator """
def create_b_location():
	blocation_destination = gen_coordinates()+gen_hex_code(8)
	blocation = alocation = """ "b_party_location": { "destination": "%s"}""" % (blocation_destination)
	return blocation

""" Event Details variables """
def create_event_details():
	alocation = create_a_location()
	event_d_a_number = str(random.randint(3000000000, 3069999999))
	event_d_roaming = roming_enum[random.randint(0,1)]
	if service_to_use == 2:
		event_d_access_point_name = access_point_name_enum[random.randint(0,8)]
		event_details = """\
"event_details": { "access_point_name": "%s", \
"is_roaming": %s, "a_party_number": "%s", %s }\
""" % (event_d_access_point_name, event_d_roaming, event_d_a_number, alocation)

	else:
		event_d_traffic_case = traffic_case_enum[random.randint(0,2)]
		event_d_b_number = str(random.randint(3000000000, 3069999999))
		blocation = create_b_location()
		event_d_event_type = event_type_enum[random.randint(0,3)]
		event_details = """\
"event_details": {"traffic_case": "%s", %s, "b_party_number": "%s", \
"event_type": "%s", "is_roaming": %s, %s, "a_party_number": "%s" }\
""" % (event_d_traffic_case, alocation, event_d_b_number, event_d_event_type, \
		event_d_roaming, blocation, event_d_a_number)

	return event_details

def gen_coordinates():
	return ''.join([random.choice('732103456') for x in range(6)])

""" Generate random hexa code """
def gen_hex_code(amount):
	return ''.join([random.choice('0123456789abcdef') for x in range(amount)])

""" Generate random timestamp """
def started_at_time():
	mounth=random.randint(1, 12)
	mounth_str=str(mounth)
	if mounth < 10: mounth_str="0"+str(mounth)
	if mounth == 2: day=random.randint(1, 28)
	else: day=random.randint(1, 30)
	day_str = str(day)
	if day < 10: day_str = "0"+str(day)
	hour=random.randint(0, 23)
	hour_str = str(hour)
	if hour < 10: hour_str = "0"+str(hour)
	timestamp = "%s-%s-%sT%s:%s:%s" % (str(random.randint(2015, 2017)), mounth_str,\
	day_str, hour_str, str(random.randint(10,59)), str(random.randint(10,59)))
	return timestamp

""" EDR table """
def create_edr_table(event_details, event_charges, service_unit, edr_service_use):
	edr_id = gen_hex_code(30) #"006ef78034fff173e2810863037702"
	edr_service = str(edr_service_use)
	timestamp = started_at_time()
	#edr_created_at = str(datetime.datetime.now()) #+str() #"2016-01-13T 14:33:37.000Z"
	#edr_created_at = edr_created_at[:19]
	edr_created_at = timestamp # edr_created_at.replace(" ", "T")
	#edr_started_at = str(datetime.datetime.now())
	#edr_started_at = edr_started_at[:19] #"2016-01-13T 14:33:37.000Z"
	edr_started_at = timestamp # edr_started_at.replace(" ", "T")
	edr = """\
"edr": {"id": "%s", "service": "%s", %s, "created_at": "%s", "started_at": "%s", %s, %s }\
""" % (edr_id, edr_service, event_details, edr_created_at, edr_started_at, event_charges, service_unit)

	""" Table handling """
	edr_table = """{%s}""" % (edr)
	return edr_table

""" Writes the json entries to a file """
def write_mocdata_to_a_file(edr_list_json, i):
	dir_path = os.path.dirname(os.path.realpath(__file__))
	file = open("%s/../dataModel/mockdata-%d.json" % (str(dir_path),i), "w")
	file.write(edr_list_json)
	file.close()
	#bashCommand = "uname -n"
	#process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
	#output, error = process.communicate()

""" Create database entries for testing, and handling the EDR list """
def create_database_entries(argument):
	split_amount = int(argument/4)
	edr_arr = []
	edr_list = []
	edr_list_json = []
	for i in range(0, argument):
		edr_service = random.randint(1, 2)
		set_global_var(edr_service)
		service_unit_t = create_service_unit()
		edr_table = create_edr_table(create_event_details(), \
			create_event_charges(service_unit_t), service_unit_t, edr_service)
		edr_list.append(edr_table)
		if int(len(edr_list)) == split_amount:
			edr_arr.append(edr_list)
			edr_list = []

	for mocdata_list in edr_arr:
		edr_list_json.append((""" %s """ % (mocdata_list)).replace("\'", ""))

	return edr_list_json

""" Assigns a value to the global variable """
def set_global_var(value):
	global service_to_use
	service_to_use = value

def main(argv):
	""" Starts the timer """
	t0 = time.clock()
	amount = arg_t(argv)

	""" Creates entries and writes them to a json file """
	mocdata = create_database_entries(amount)
	i = 0
	for entrys in mocdata:
		write_mocdata_to_a_file(entrys, i)
		i = i + 1
	""" Stops the timer """
	t1 = (time.clock() - t0)
	print "Done! Time taken: %s sec" % (t1)

""" Start of the program """
if __name__ == "__main__":
	main(sys.argv[1:2])
