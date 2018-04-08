#!python3

from sessionization import Sessionization
from helper import command_parser
import os, sys, argparse




def main():
	"""
		containts call to major impt funtions!
	"""
	passed_files = command_parser()
	data = passed_files["logcsv"]
	inactivity_file = passed_files["inactivity"]
	session_file = passed_files["session"]

	ss = Sessionization(data,inactivity_file,session_file)
	#ss.read_csv()
	#ss.read_csv_as_dict()
	#ss.print_data()  
	#ss.read_csv_to_dict()
	ss.read_csv_pandas()
	print("\n")
	ss.get_time_ip_document()



if __name__ == "__main__":

    main()