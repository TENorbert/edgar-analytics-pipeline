#!python3

from sessionization import analyze
from helper import command_parser, get_inactivity_period, get_data_lines
import os, sys, argparse




def main():
	"""
		containts call to major impt funtions!
	"""
	inactivity_period = 0

	passed_files = command_parser()
	data_file = passed_files["logcsv"]
	inactivity_file = passed_files["inactivity"]
	session_file = passed_files["session"]

	inactivity_period = get_inactivity_period(inactivity_file)
	print(inactivity_period)

	lines = get_data_lines(data_file)
	analyze(lines)
	



if __name__ == "__main__":

    main()