#!python3


# helper.py
# contains helper fuctions
#
import os, sys, argparse


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


def get_input_files():
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

'''
if __name__=="__main__":
		from sys import argv
		myargs = getopts(argv)
		if '-i' in myargs:
		print(myargs['-i'])
		print(myargs)
    
    #files  = {}
    #files = command_parser()
    #print(files["logcsv"],files["inactivity"], files["inactivity"] )
'''