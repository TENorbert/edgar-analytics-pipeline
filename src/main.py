#!python3

from sessionization import analyze
from helper import command_parser, get_inactivity_period, get_data_lines
import os, sys, argparse




def main():
	"""
		main with call to major impt funtions!
	"""
	passed_files = command_parser()
	data_file = passed_files["logcsv"]
	inactivity_file = passed_files["inactivity"]
	session_file = passed_files["session"]

	inactivity_period = int(get_inactivity_period(inactivity_file))
	#print(inactivity_period)

	#lines = get_data_lines(data_file)
	analyze(data_file, inactivity_period)
	


if __name__ == "__main__":

    main()