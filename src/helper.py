#!python3


# helper.py
# contains helper fuctions
#
import os, sys, argparse
import pandas as pd 
import numpy as np 
import csv 

from datetime import datetime
from dateutil.parser import parse
import math
#import subprocess  # using linux like stuff



def command_parser():
	'''
		command line passing arguments
	'''
	ifile = ''
	inacfile = ''
	ofile = ''
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--logcsv", required=True, help="input log.csv file")
	ap.add_argument("-a", "--inactivity", required=True, help="input inactivity.txt file")
	ap.add_argument("-o", "--session", required=True, help="output sessionization.txt file")
	args = vars(ap.parse_args())
	#print(args)
	ifile = args["logcsv"]
	inacfile = args["inactivity"]
	ofile = args["session"]
	#print("Input File = {0}".format(ifile))
	#print("Inactivity File = {0}".format(inacfile)
	#print("Output File = {0}".format(ofile))
	return args


def read_input_files():
	'''
	   Method to read input files without passing path to file
	   NB: Be careful which directiory you are..I know could make it better!
	'''
	#ifile = "./input/log.csv"
	#inacfile = "./input/inactivity_period.txt"
	#ofile = "./output/sessionization.txt" 
	files = {}
	path = '.' # if runing as python ./src/main.py,  else path = ".." 
	ifile = os.path.join(path, "input", 'log.csv')
	inacfile =  os.path.join(path, "input", 'inactivity_period.txt')
	ofile = os.path.join(path, "output", 'sessionization.txt')
	file["logcsv"] = ifile
	file["inactivity"] = inacfile
	file["session"] = ofile

	return files



def read_csv(csv_filename):
	"""
         Read cvs file with header byt skipping the first line(header line)
         and returns a list of all the lines read
    """
	csv_rows = []
	try:
		csv_fobj = open(csv_filename)
		readobj = csv.reader(csv_fobj)
		for row in readobj:
			if readobj.line_num == 1:
				continue
			csv_rows.append(row)
	except Exception as e:
		msg = "Can't read csv file {}".format(csv_filename)
		print(msg)

	return csv_rows


def write_data_to_file(file_name='./output/sessionization.txt', *data):
	'''
		Takes given data and writes the data to txt file
		append each time.
		Default file path is '..'
	'''
	f_obj = open(file_name, 'a')
	for d in data:
		if d == "\n":
			f_obj.write(str(d))
		else:
			f_obj.write(str(d) + ",")
	f_obj.close()


def get_inactivity_period(file_name):
	'''
	 	Read single variable in file e.g inactivity_perion.txt file
	 	Return: value (single value read from file)
	'''
	value = -1
	try:
		with open(file_name, 'r') as f_obj:
		    for line in f_obj: # one line at a time(More efficient)
		        line = line.strip()
		        split_line = line.split(",") #split row with comma seperated.
		        value = split_line[0]
		return value
	except Exception:
		print("Unable to open file = {}".format(file_name))



def create_date_time(date_str, time_str):
	'''
		Takes date and time as string and creates a datetime object
	'''
	try:
		dt_obj = datetime.now().strftime('%Y-%b-%d:%H:%M:%S')
		if isinstance(date_str, str) and isinstance(time_str, str):
			dt_str = date_str + ":" + time_str
			dt_obj = datetime.strptime(dt_str, '%Y-%m-%d:%H:%M:%S')
		else:
			dt_str = str(date_str) + ":" + str(time_str)
			dt_obj = datetime.strptime(dt_str, '%Y-%m-%d:%H:%M:%S')
	except Exception as e:
		print(e, type(e))

	#return dt_obj.strftime('%Y-%m-%d:%H:%M:%S')
	return str(dt_obj.strftime('%Y-%m-%d:%H:%M:%S'))


def create_request_document(cik_str, acc_str, ext_str):
	'''
	   The project github page said we can assume that:
	   a single web page request document = combination( cik, accession, extention)
	   Takes cik, accession, extention and creates a foul request coument
	'''
	try:
		if isinstance(cik_str, str) and isinstance(acc_str, str) and isinstance(ext_str, str):
			return (cik_str + "" + acc_str + "" + ext_str)
		else:
			return (str(cik_str) + "" + str(acc_str) + "" + str(ext_str))
	except Exception as e:
		print(e, type(e))



def get_elapse_time(time_1_obj, time_2_obj):
	'''
		Takes two datetime objects and return their difference(in seconds)
		as time elapse
		NB: Although this function does not care about order but please
			make sure time_2_obj is later than time_1_obj
	'''
	elapse_time = -99
	try:
		if isinstance(time_1_obj, datetime) and isinstance(time_2_obj, datetime):
			if time_2_obj > time_1_obj:
			    elapse_time = (time_2_obj - time_1_obj).seconds
			else:
				elapse_time = (time_2_obj - time_1_obj).seconds
		else:
			dt1  = datetime.strptime(time_1_obj, '%Y-%m-%d:%H:%M:%S')
			dt2 = datetime.strptime(time_2_obj, '%Y-%m-%d:%H:%M:%S')
			elapse_time = (dt2 - dt1).seconds
	except Exception as e:
		print(e, type(e))

	return int(elapse_time)



def has_session_ended(time_1_obj, time_2_obj, inactivity_period=2):
	'''
		Takes two date time and check if their elapse
		time is greater than the session inactivity_period(default = 2 seconds)
		The session inactivity_period if from inactivity_period.
		Returns True if duration >= inactivity_period
		        else False
	'''
	try:
		user_duration = get_elapse_time(time_1_obj, time_2_obj)
		if user_duration >= inactivity_period:
			return True
		else:
			return False
	except Exception as e:
		print(e, type(e))



def is_less_than(time_1_obj, time_2_obj):
	'''
		Takes two datetime objects and return True if time_1_obj < time_2_obj
		else false
		NB: Order matters else you'r on ur own!
			make sure time_2_obj is later than time_1_obj
	'''
	try:
		if isinstance(time_1_obj, datetime) and isinstance(time_2_obj, datetime):
			if time_2_obj > time_1_obj:
			    return True
			else:
			    return False
	except Exception as e:
		print(e, type(e))


def reverse_stack(stack):
	'''
	  Takes an imput stack and reverses its content using a list
	:param stack:
	:return: Reversed Stack
	'''
	items = []
	while not stack.is_empty():
		items.append(stack.pop())

	for item in items:
		stack.push(item)


#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
def read_csv_as_list(csv_filename, field_name):
	'''
		Reads column from csv file & returns list for values
		of the column
		Returns: list of Column elements
	'''
	column_list = []
	try:
		with open(csv_filename, 'r') as f_obj:
		    #lines = f_obj.readlines()[1:] #skip first line
		    next(f_obj) # skip column title/first line
		    for line in f_obj: # efficient
		        line = line.strip()
		        split_line = line.split(",") #split row with comma seperated.
		        if len(split_line) == 15:
		        	if field_name == 'ip':
		        	    column_list.append(split_line[0])
		        	elif field_name == 'date':
		        	    column_list.append(split_line[1])
		        	elif field_name == 'time':
		        	    column_list.append(split_line[2])
		        	elif field_name == 'cik':
		        	    column_list.append(split_line[4])
		        	elif field_name == 'accession':
		        	    column_list.append(split_line[5])
		        	elif field_name == 'extention':
		        		column_list.append(split_line[6])
		        	else:
		        		print("{} Not Found!".format(field_name))
		        else:
		        	print("Multiple or Fewer Readlines!")
		        	break
		        	
	except Exception:
		column_list = []
		#print(e, type(e))

	return column_list



def data_as_df(csv_data_file):
    """
        Use Pandas dataframe to read csv input file and store
        read data as a pandas dataframe.
        NB: requires Pandas, module installed.
    """
    data_df = {}
    try:
        # Read Data into Dataframe and skip first/header row!!
        data_df = pd.read_csv(csv_data_file, skiprows=0)
    except Exception as e:
        print(e,type(e))

    return data_df 



def list_from_df(data_df, data_key):
	"""
	   uses the data_key or column to return the
	   corresponding values to the data_key from pandas data frame(data_df)
	   could also read a pandas object directly
	"""
	data_column = data_df[data_key]
	# make sure the data column has same length as at least the fist column.
	# nice to look for the most important column such as index_ID in pandas
	if len(data_column) == len(data_df['ip']):
		return data_column
	else:
		print("data field for field {0} has number of element = {1}".format(data_key, len(data_column)))



def list_from_datafile(data_csv_file, field_name):
    """
        Reads a cvs file using the DictReader method which
        is faster and mmemory efficient using generators.
        Returns list for given column
    """
    column_list = []
    try:
        with open(data_csv_file, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
            	column_list.append(row[field_name])
    except Exception as e:
        msg = "Can't read csv file {}".format(filename)
        print(msg)

    return column_list

def data_as_dict(csv_data_file):
    """
        Use Pandas dataframe to read csv input file and store
        read data as a dictionary of lists.
        NB: requires Pandas, module installed.
    """
    data_dict = {}
    try:
        # Read Data into Dataframe and skip first/header row!!
        df = pd.read_csv(csv_data_file, skiprows=0)
        #create dictionary using column names as keys and values as list of column data
        data_dict = df.to_dict()
        #for key, value in data_dict.items():
        #   print("key = {0} , value = {1}".format(key, value))
    except Exception as e:
        print(e,type(e))

    return data_dict


def list_from_dict(data_dict, data_key):
	"""
	   Uses the data_key or column to return the
	   corresponding values(as dictionaries whose 
	   keys are Pandas Index numbers produced from
	   data_to_dict() fcn above) to the data_key from data dictionary
	   could also read a pandas object directly
	   NB: To access each value for keys, must loop as a dictionary
	   in the resulting return object(mini Dictionary)
	   e.g 
	   		d = data_as_dict(files["logcsv"])
    		#print(d)
    		zone_dict = list_from_dict(d, 'zone')
    		for zone,value in zone_dict.items():
    		print("key : " + str(zone) + " , " + "value : " + str(value))
    		#print(zone_list)
	"""
	data_column = data_dict[data_key]
	# make sure the data column has same length as at least the fist column.
	return data_column





def read_csv_to_dict(csv_filename):
	"""
		Reads data from cvs log files using 
		strip and split() functions
		Returns Dictionary of as data read
		NB: Not a very scalable solution
	"""
	data_dict = {}
	ip_list = []
	date_list = []
	time_list = []
	cik_list = []
	acession_list = []
	ext_list = []
	#zone_list = []
	#code_list = []
	#size_list = []
	#idx_list = []
	#norefer_list = []
	#noagent_list = []
	#find_list = []
	#crawler_list = []
	#browser_list = []
	try:
		with open(csv_filename, 'r') as f_obj:
		    #lines = f_obj.readlines()[1:] #skip first line
		    #print("Total Number of lines in file = {0}".format(len(lines)))
		    next(f_obj) # skip column title/first line
		    for line in f_obj: # one line at a time(More efficient)
		        line = line.strip()
		        split_line = line.split(",") #split row with comma seperated.
		        if len(split_line) < 15:
		    	    print("Missing Column!")
		    	    break
		        else:
		        	ip_list.append(split_line[0])
		        	date_list.append(split_line[1])
		        	time_list.append(split_line[2])
		        	cik_list.append(split_line[4])
		        	acession_list.append(split_line[5])
		        	ext_list.append(split_line[6])

		        	#zone_list.append(split_line[3])
		        	#code_list.append(split_line[7])
		        	#size_list.append(split_line[8])
		        	#idx_list.append(split_line[9])
		        	#norefer_list.append(split_line[10])
		        	#noagent_list.append(split_line[11])
		        	#find_list.append(split_line[12])
		        	#crawler_list.append(split_line[13])
		        	#browser_list.append(split_line[14])
		        	#print(split_line[0])
	except Exception as e:
		msg = "Can't read csv file {}".format(csv_filename)
		print(msg)

	data_dict['ip'] = ip_list
	data_dict['date'] = date_list
	data_dict['time'] = time_list
	data_dict['cik'] = cik_list
	data_dict['accession'] = acession_list
	data_dict['extention'] = ext_list

	#data_dict['zone'] = zone_list
	#data_dict['code'] = code_list
	#data_dict['size'] = size_list
	#data_dict['idx'] = idx_list
	#data_dict['norefer'] = norefer_list
	#data_dict['noagent'] = noagent_list
	#data_dict['find'] = find_list
	#data_dict['crawler'] = crawler_list
	#data_dict['browser'] = browser_list

	return data_dict



def add_to_dataframe(data_frame, column_list, field_name):
	"""
		Adds new column with list to data frame
		Input: DataFrame, column_list, field_name
		Return: Nothing
	"""
	try:
	    data_frame[field_name] = column_list
	except Exception as e:
		print(e, type(e))


def add_to_dict(data_dict, column_list, field_name):
	"""
		Adds new column with list to data frame
		Input: DataFrame, column_list, field_name
		Return: Nothing
	"""	
	try:
	    data_dict[field_name] = column_list
	except Exception as e:
		print(e, type(e))





def get_last_row(file_name):
	'''
	 Returns the last row of a file
	'''
	f_obj = open(file_name, 'r')
	last_line = subprocess.check_output("tail", "-1", file_name)
	last = [ x for x in last_line.split(',')[2:]]

	if len(last_row) == 15:
		last_row = last
	else:
		print("last row has length = {}".format(len(last_row)))

	f_obj.close()

	return last_row




def get_csv_data(csv_filename):
    """
        Reads a cvs file using the DictReader method which
        is faster and mmemory efficient using generators.
    """
    try:
        with open(csv_filename, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            #for row in csv_reader:
           		#print(row)
    except Exception as e:
        msg = "Can't read csv file {}".format(csv_filename)
        print(msg) 



def get_data_lines(data_file):
	'''
	   Reads cvs files as lines(not very efficient esp for large files as
	   it reads all the lines at once!)
	   Returns: lines read from file
	'''
	try:
		with open(data_file, 'r') as f_obj:
			next(f_obj) #skip header line
			lines = f_obj.readlines()
		return lines
	except Exception:
		print("Can't open file = {}".format(data_file))



if __name__=="__main__":
	
    files  = {}
    files = command_parser()
    #print(files["logcsv"],files["inactivity"], files["inactivity"] )
    ip_address = list_from_datafile(files["logcsv"], 'ip')
    #print(ip_address)
    #data = data_from_csv_as_dict(files["logcsv"])
    inactivity_period = get_inactivity_period(files["inactivity"])
    print(inactivity_period)
    #print(data)
    #print(data['ip'])
    #print(len(data['zone']))
    #df = data_as_df(files["logcsv"])
    #zone_list = list_from_df(df, 'zone')
    #print(zone_list)

    d = data_as_dict(files["logcsv"])
    #print(d)
    time_dict = list_from_dict(d, 'time')

    #for time,value in time_dict.items():
    #	print("key : " + str(time) + " , " + "value : " + str(value))
    #print(zone_dict)
    dt = read_csv_to_dict(files["logcsv"])
    #print(len(dt['ip']))
    f_name = 'test_file.txt'; 
    write_data_to_file(f_name, str(dt['ip']))
    #dm = data_from_csv_as_dict(files["logcsv"])

    date_list = read_csv_as_list(files["logcsv"], 'date')
    time_list = read_csv_as_list(files["logcsv"], 'time')

    time_obj1 = create_date_time(date_list[0], time_list[0] )
    time_obj0 = create_date_time(date_list[5], time_list[5] )

    time_obj2 = create_date_time(date_list[7], time_list[7] )

    duration = get_elapse_time(time_obj0, time_obj2)
    if (has_session_ended(time_obj0,time_obj2)):
    	print("Session with {} has ended".format(time_obj0))
    else:
    	print("Session with {} has Not ended".format(time_obj0))

    print("Time Elapse is {}".format(duration))
    #date_time = [ time_obj = datetime.strptime(time_str, '[%d/%b/%Y:%H:%M:%S %z]')]
    #print(date_list)
    
    #data_read = read_csv(files["logcsv"])
    #for i in range(len(data_read)):
    #	print("length = {} and list = {} \n".format(len(data_read[i]), data_read[i]))

    #print(data_read[-1])