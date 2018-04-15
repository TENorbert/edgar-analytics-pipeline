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

	weblog_elements = []  #Q.PriorityQueue() # Testing using PQueues

	weblog_queue = Q.PriorityQueue()  ## scalability

	#lines = get_data_lines(data_file)
	analyze(data_file, weblog_elements, weblog_queue, inactivity_period)

	# Print out using Queue
	#print("weblog_elements length = {0}".format(weblog_elements.qsize()))
	print("weblog_elements length = {0}".format(len(weblog_elements)))

	#while not weblog_elements.empty():
	for cur_weblog in weblog_elements:
		#cur_weblog = weblog_elements.get()
		#print(cur_weblog)
		print("{0}, {1}, {2}, {3}, {4}, {5} \
	        ".format(cur_weblog.ip_address, cur_weblog.start_datetime,
			cur_weblog.end_datetime, cur_weblog.request_document,
			cur_weblog.duration, cur_weblog.doc_number)
			)
	print("\n")
	# Print Queue content
	print("weblog_queue has {0} weblogs for output".format(weblog_queue.qsize()))
	while not weblog_queue.empty():
		cur_weblog = weblog_queue.get()
		# print(cur_weblog)
		print("{0}, {1}, {2}, {3}, {4}, {5} \
	            ".format(cur_weblog.ip_address, cur_weblog.start_datetime,
				cur_weblog.end_datetime, cur_weblog.request_document,
				cur_weblog.duration, cur_weblog.doc_number)
			  )


if __name__ == "__main__":

	main()