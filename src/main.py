#!python3

from sessionization import analyze
from helper import command_parser, get_inactivity_period, get_data_lines
import os, sys, argparse

try:
    import Queue as Q # ver. < 3.0
except ImportError:
    import queue as Q




def main():
	"""
		main with call to major impt funtions!
	"""
	passed_files = command_parser()
	data_file = passed_files["logcsv"]
	inactivity_file = passed_files["inactivity"]
	session_file = passed_files["session"]
	inactivity_period = int(get_inactivity_period(inactivity_file))

	read_weblogs = []  #Q.PriorityQueue() # Testing using PQueues

	output_weblogs = Q.Queue()  ## scalability

	#lines = get_data_lines(data_file)
	analyze(data_file, read_weblogs, output_weblogs, inactivity_period)

	# Print out using Queue
	#print("read_weblogs length = {0}".format(read_weblogs.qsize()))
	print("read_weblogs length = {0}".format(len(read_weblogs)))

	#while not read_weblogs.empty():
	for cur_weblog in read_weblogs:
		#print(cur_weblog)
		print("{0}, {1}, {2}, {3}, {4}, {5} \
			    ".format(cur_weblog.ip_address, cur_weblog.start_datetime,
				cur_weblog.end_datetime, cur_weblog.request_document,
				cur_weblog.duration, cur_weblog.doc_number)
			  )

	print("\n")
	# Print Queue content
	print("Output_weblogs has {0} weblogs for output".format(output_weblogs.qsize()))
	print("======================================================================")
	while not output_weblogs.empty():
		cur_weblog = output_weblogs.get()
		# print(cur_weblog)
		print("{0}, {1}, {2}, {3}, {4}\
			    ".format(cur_weblog.ip_address, cur_weblog.start_datetime,
				cur_weblog.end_datetime, cur_weblog.duration, cur_weblog.doc_number)
			  )
	print("======================================================================")



if __name__ == "__main__":

	main()