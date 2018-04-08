#!python3


# helper.py
# contains helper fuctions
#
import os, sys, argparse
import pandas as pd 
import numpy as np 
import csv 



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



def list_from_datafile(data_csv_file, column_name):
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
            	column_list.append(row[column_name])
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



def write_data_to_file(file_name='./output/sessionization.txt', *data):
	'''
		Takes given data and writes the data to txt file
		append each time.
		Default file path is '..'
	'''
	f_obj = open(file_name, 'a')
	for d in data:
		f_obj.write(d)

	f_obj.close()


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
	zone_list = []
	cik_list = []
	acession_list = []
	ext_list = []
	code_list = []
	size_list = []
	idx_list = []
	norefer_list = []
	noagent_list = []
	find_list = []
	crawler_list = []
	browser_list = []
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
		        	zone_list.append(split_line[3])
		        	cik_list.append(split_line[4])
		        	acession_list.append(split_line[5])
		        	ext_list.append(split_line[6])
		        	code_list.append(split_line[7])
		        	size_list.append(split_line[8])
		        	idx_list.append(split_line[9])
		        	norefer_list.append(split_line[10])
		        	noagent_list.append(split_line[11])
		        	find_list.append(split_line[12])
		        	crawler_list.append(split_line[13])
		        	browser_list.append(split_line[14])
		        	#print(split_line[0])
	except Exception as e:
		msg = "Can't read csv file {}".format(csv_filename)
		print(msg)

	data_dict['ip'] = ip_list
	data_dict['date'] = date_list
	data_dict['time'] = time_list
	data_dict['zone'] = zone_list
	data_dict['cik'] = cik_list
	data_dict['accession'] = acession_list
	data_dict['extention'] = ext_list
	data_dict['code'] = code_list
	data_dict['size'] = size_list
	data_dict['idx'] = idx_list
	data_dict['norefer'] = norefer_list
	data_dict['noagent'] = noagent_list
	data_dict['find'] = find_list
	data_dict['crawler'] = crawler_list
	data_dict['browser'] = browser_list

	return data_dict

## Not working as wanted
def data_from_csv_as_dict(csv_filename):
    """
        Reads a cvs file using the DictReader method which
        is faster and mmemory efficient using generators.
    """
    data_dict = {}
    try:
        with open(csv_filename, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:            	
            	#print(row)
            	#data_dict.update(row)
            	'''
            	data_dict['ip'] = row['ip']
            	data_dict['date'] = row['date']
            	data_dict['time'] = row['time']
            	data_dict['zone'] = row['zone']
            	data_dict['cik'] = row['cik']
            	data_dict['accession'] = row['accession']
            	data_dict['extention'] = row['extention']
            	data_dict['code'] = row['code']
            	data_dict['size'] = row['size']
            	data_dict['idx'] = row['idx']
            	data_dict['norefer'] = row['norefer']
            	data_dict['noagent'] = row['noagent']
            	data_dict['find'] = row['find']
            	data_dict['crawler'] = row['crawler']
            	data_dict['browser'] = row['browser']
            	'''
    except Exception as e:
        msg = "Can't read csv file {}".format(csv_filename)
        print(msg) 

    if len(data_dict) != 0:
    	return data_dict


def read_csv(csv_filename):
    """
     	Reads a csv file and creates a dictionary
    """
    try:
        with open(csv_filename, 'r') as cvs_file:
            csv_reader = csv.reader(cvs_file)
            next(csv_reader) # skip header line!
            print(cvs_reader)
    except Exception as e:
        msg = "Can't read csv file {}".format(csv_filename)
        print(msg) 

	


if __name__=="__main__":
	
    files  = {}
    files = command_parser()
    #print(files["logcsv"],files["inactivity"], files["inactivity"] )
    ip_address = list_from_datafile(files["logcsv"], 'ip')
    #print(ip_address)
    data = data_from_csv_as_dict(files["logcsv"])
    #print(data)
    #print(data['ip'])
    #print(len(data['zone']))
    #df = data_as_df(files["logcsv"])
    #zone_list = list_from_df(df, 'zone')
    #print(zone_list)

    d = data_as_dict(files["logcsv"])
    #print(d)
    zone_dict = list_from_dict(d, 'time')
    #for zone,value in zone_dict.items():
    #	print("key : " + str(zone) + " , " + "value : " + str(value))
    #print(zone_dict)
    dt = read_csv_to_dict(files["logcsv"])
    print(len(dt['ip']))
    f_name = 'test_file.txt'; 
    write_data_to_file(f_name, str(dt['ip']))
    
