
import csv 
import numpy as np 
import pandas as pd
import unittest



class Sessionization(object):
    """
      Reads Data from input log files and 
      produces session timeout time for each unqiue user.
      Each Unique user is identified by a unique Ip Address
      All relevatn variables are read from a Weblog csv file
    """
    #def __init__(self, ifile, inacfile, ofile):
    def __init__(self, ifile, inacfile, ofile):
        self.parameter_dict = {} # creates initial dictionary with keys as parameters(columns) and values as(records or list of values)
        self.start_time = []  #list of time
        self.ip_address = []  #list of ip_address
        self.document_number = [] #list of document number
        self.ifile = ifile
        self.inacfile = inacfile
        self.ofile = ofile



    def read_csv_pandas(self):
        """
           Use Pandas dataframe to read csv input file and store
           read data as a dictionary of lists.
           NB: requires Pandas, numpy module installed.
        """
        try:
            # Read Data into Dataframe and skip first/header row!!
            df = pd.read_csv(self.ifile, skiprows=0)
            #create dictionary using column names as keys and values as list of column data
            self.parameter_dict = df.T.to_dict('list') 
            for key in self.parameter_dict.keys():
               print("{0}:{1}".format(key, self.parameter_dict[key]))
            

            self.ip_address = self.parameter_dict.get('ip',0)
            self.start_time = self.parameter_dict.get('time',0)
            self.document_number = self.parameter_dict.get('extention',0)

            print("documents = {0}".format(self.document_number))
            print("Start Time = {0}".format(self.start_time))
            print("IP Address = {0}".format(self.ip_address))
        except Exception as e:
            print(e,type(e))

    def get_time_ip_document(self):
        self.ip_address = self.parameter_dict.get('ip',0)
        self.start_time = self.parameter_dict.get('time',0)
        self.document_number = self.parameter_dict.get('extention',0)

        print("documents = {0}".format(self.document_number))
        print("Start Time = {0}".format(self.start_time))
        print("IP Address = {0}".format(self.ip_address))


    def read_csv(self):
        """
         Reads a csv file and creates a dictionary
        """
        try:
            with open(self.ifile, 'r') as cvs_file:
                csv_reader = csv.reader(cvs_file)
                next(csv_reader) # skip header line!
                self.create_data_dict(csv_reader)
        except Exception as e:
            msg = "Can't read csv file {}".format(self.ifile)
            print(msg) 

    def create_data_dict(self, cvs_handle):
        """
            creates that data dictionary from cvs_reader.
        """
        try: 
            for row in cvs_handle:
                #print(row[0])
                #print(len(row[0]))
                self.parameter_dict['ip'] = row[0]
                self.parameter_dict['date'] = row[1]
                self.parameter_dict['time'] = row[2]
                self.parameter_dict['zone'] = row[3]
                self.parameter_dict['cik'] = row[4]
                self.parameter_dict['accession'] = row[5]
                self.parameter_dict['extention'] = row[6]
                self.parameter_dict['code'] = row[7]
                self.parameter_dict['size'] = row[8]
                self.parameter_dict['idx'] = row[9]
                self.parameter_dict['norefer'] = row[10]
                self.parameter_dict['noagent'] = row[11]
                self.parameter_dict['find'] = row[12]
                self.parameter_dict['crawler'] = row[13]
                self.parameter_dict['browser'] = row[14]

        except Exception as e:
            print(e, type(e)) 


    def read_csv_as_dict(self):
        """
         Reads a cvs file using the DictReader method which
         is faster and mmemory efficient using generators.
        """
        try:
            with open(self.ifile, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    self.parameter_dict['ip'] = row['ip']
                    self.parameter_dict['date'] = row['date']
                    self.parameter_dict['time'] = row['time']
                    self.parameter_dict['zone'] = row['zone']
                    self.parameter_dict['cik'] = row['cik']
                    self.parameter_dict['accession'] = row['accession']
                    self.parameter_dict['extention'] = row['extention']
                    self.parameter_dict['code'] = row['code']
                    self.parameter_dict['size'] = row['size']
                    self.parameter_dict['idx'] = row['idx']
                    self.parameter_dict['norefer'] = row['norefer']
                    self.parameter_dict['noagent'] = row['noagent']
                    self.parameter_dict['find'] = row['find']
                    self.parameter_dict['crawler'] = row['crawler']
                    self.parameter_dict['browser'] = row['browser']
        except Exception as e:
            msg = "Can't read csv file {}".format(self.ifile)
            print(msg) 



    def print_data(self):
        """
            prints dictionary content for debugging/testing purposes
        """
        if self.parameter_dict != {}:
            #for key,values in self.parameter_dict.items():
            #    print(key + " : " + values)
            for k in self.parameter_dict.keys():
                print(self.parameter_dict[k])
            #print(self.parameter_dict)
            for value in self.parameter_dict.values():
                print(value)

        else:
            print("Empty dictionary Found!")

    # Read into dictionary using readlines
    def read_csv_to_dict(self):
        try:
            with open(self.ifile, 'r') as f_obj:
                #lines = f_obj.readlines()[1:] #skip first line
                #print(lines)
                #print("Total Number of lines in file = {0}".format(len(lines)))
                next(f_obj) # skip column title/first line
                for line in f_obj: # one line at a time(More efficient)
                    line = line.strip()
                    split_line = line.split(",") #split row with comma seperated.
                    if len(split_line) < 15:
                        print("Missing Column!");
                        self.parameter_dict = {}
                        break
                    else:
                        self.parameter_dict['ip'] = split_line[0]
                        self.parameter_dict['date'] = split_line[1]
                        self.parameter_dict['time'] = split_line[2]
                        self.parameter_dict['zone'] = split_line[3]
                        self.parameter_dict['cik'] = split_line[4]
                        self.parameter_dict['accession'] = split_line[5]
                        self.parameter_dict['extention'] = split_line[6]
                        self.parameter_dict['code'] = split_line[7]
                        self.parameter_dict['size'] = split_line[8]
                        self.parameter_dict['idx'] = split_line[9]
                        self.parameter_dict['norefer'] = split_line[10]
                        self.parameter_dict['noagent'] = split_line[11]
                        self.parameter_dict['find'] = split_line[12]
                        self.parameter_dict['crawler'] = split_line[13]
                        self.parameter_dict['browser'] = split_line[14]
                        #print(split_line[0])
                        #print(split_line[1])
                        #print(split_line[2])

                #print("Single line length = {0}".format(len(self.parameter_dict['ip'])))
                #print("Single line = {0}".format(self.parameter_dict['ip'])) 
                print(self.parameter_dict)
        except Exception as e:
            msg = "Can't read csv file {}".format(self.ifile)
            print(msg)


    def compute_inactivity(self):
         pass

    