#!python3

from sessionization import VisitorActivity, VisitorReport
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

	vis_act = Weblog()
	vis_act.compute_elapsed_time()
	vis_act.compute_inactivity()

	vis_report = VisitorReport()
	vis_report.generate_report()



if __name__ == "__main__":

    main()