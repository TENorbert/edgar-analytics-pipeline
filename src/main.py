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
		main function
	"""
	try:
		passed_files = command_parser()
		data_file = passed_files["logcsv"]
		inactivity_file = passed_files["inactivity"]
		session_file = passed_files["session"]
		inactivity_period = int(get_inactivity_period(inactivity_file))

		read_weblogs = [] #data structure for read weblogs
		#read_weblogs = Q.PriorityQueue() # Testing using PQueues

		output_weblogs = Q.Queue() #output data structure for session ended weblogs, some entry priority? & scalability?
		#output_weblogs = Q.PriorityQueue()

		analyze(data_file, read_weblogs, output_weblogs, inactivity_period)

		#Print out using Queue
		#print("read_weblogs length = {0}".format(read_weblogs.qsize()))
		print("read_weblogs length = {0}".format(len(read_weblogs)))


		print("======================================================================")
		print("Output_weblogs length = {0}".format(output_weblogs.qsize()))

		output_filename = session_file
		#output_filename = os.path.join('./', 'test_output_file.txt')
		print("Writing output to file = {0}!\n".format(output_filename))
		#write_output(output_weblogs, output_filename)
		with open(output_filename, 'a') as f_obj:
			#f_obj.write("Output_weblogs length = {0} \n".format(output_weblogs.qsize()))
			while not output_weblogs.empty():
				cur_weblog = output_weblogs.get()
				f_obj.write(str(cur_weblog.ip_address) + ',' + str(cur_weblog.start_datetime) + ','
						+ str(cur_weblog.end_datetime) + ',' + str(cur_weblog.duration) + ','
						+ str(cur_weblog.get_document_number()) + "\n"
						)

		print("Writing to output file ends!")
		print("======================================================================")


		'''
		#Debugging!
		#while not read_weblogs.empty():
		for cur_weblog in read_weblogs:
			#print(cur_weblog)
			print("{0}, {1}, {2}, {3}, {4}, {5} \
					".format(cur_weblog.ip_address, cur_weblog.start_datetime,
					cur_weblog.end_datetime, cur_weblog.request_document,
					cur_weblog.duration, cur_weblog.doc_number)
				  )

		print("\n")
		#Print Queue content
		print("Output_weblogs has {0} weblogs for output".format(output_weblogs.qsize()))
		print("======================================================================")
		while not output_weblogs.empty():
			cur_weblog = output_weblogs.get()
			# print(cur_weblog)
			print("{0}, {1}, {2}, {3}, {4}\
					".format(cur_weblog.ip_address, cur_weblog.start_datetime,
					cur_weblog.end_datetime, cur_weblog.duration, cur_weblog.get_document_number())
				)
		print("======================================================================")
		#'''
	except Exception:
		print("main failed!")


if __name__ == "__main__":

	main()