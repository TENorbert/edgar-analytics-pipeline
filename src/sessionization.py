

import unittest
from helper import *  # helper functions

try:
    import Queue as Q # ver. < 3.0
except ImportError:
    import queue as Q



class Weblog(object):
    """
      Takes ip_address, dateTime, document and creates a weblog(session) Object
      session timeout time for each unqiue user(ip Address).
      Each unique user(or weblog) is identified by a unique Ip Address
    """
    
    def __init__(self, ip_address, start_date_time, end_date_time, request_document):
        self.ip_address = ip_address
        self.start_date_time = start_date_time
        self.end_date_time = end_date_time
        self.request_document = request_document
        self.document_counter = {} # Dictionary of state_date_time(key) and number of requested documents(values)
        self.session_duration = 0 # this weblog session duration (not ip!)\

    # Acessors/Getters
    def get_ip(self):
        return self.ip_address

    def get_start_date_time(self):
        return self.start_date_time

    def get_end_date_time(self):
        return self.end_date_time

    def get_request_document(self):
        return self.request_document

    def get_session_duration(self):
        return self.session_duration

    def get_document_count(self, date_time_list):
        count = 0
        for dt in date_time_list:
            count += self.document_counter[dt] # Sum length of all date times for this ip
        return count



    #M Mutators/Setters
    def set_ip(self, ip_address):  
        self.ip_address = ip_address  ## Not needed ? Why change  the IP?

    # TO DO!!
    # each time we change the start & endtime for a same ip_adress
    # shouldn't we just updated the doc request and session_duration?
    def set_start_date_time(self, start_date_time):
        self.state_date_time = start_date_time

    def set_end_date_time(self, end_date_time):
        self.set_end_date_time = end_date_time 

    def set_request_document(self, req_doc):
        self.request_document = req_doc

    def set_session_duration(self, duration):
        self.session_duration = duration


    def set_document_count(self, date_time):
        self.document_counter[date_time] = 1


    ## Aux Fxns
    def compute_session_duration(self):
        duration = get_elapse_time(self.start_date_time, self.end_date_time)
        self.session_duration = duration


'''
ip_list.append(split_line[0])
date_list.append(split_line[1])
time_list.append(split_line[2])
cik_list.append(split_line[4])
acession_list.append(split_line[5])
ext_list.append(split_line[6])
'''
def analyze(lines):
    '''
        creates dictionary of weblogs for each line
    '''
    weblog_queue = Q.PriorityQueue() ## scalability
    wl_list = []
    wl_number = 0 ## use as priority

    try:
        for line in lines:
            line = line.strip()
            llist = line.split(',')
            if len(llist) == 15:
                # now lets do all the magic
                ip_adr = llist[0]
                dt_obj = create_date_time(llist[1], llist[2])
                req_doc = create_request_document(llist[4], llist[5], llist[6])
                wl = Weblog(ip_adr, dt_obj, dt_obj, req_doc)
                #print(" Weblog.ip : " + str(wl.get_ip()) + "\n")
                weblog_queue.put((wl_number, wl))
                wl_list.append(wl)
                wl_number += 1
    except Exception as e:
        print(e, type(e))

   

    while not weblog_queue.empty():
        key, wlog = weblog_queue.get()
        print("key : " + str(key) + " Weblog.ip : " + str(wlog.get_ip()) + "\n")

        #TO DO:
        # -- Perform Analysis()
        # -- Extract Outputs(ip, startTime, endtime, duration,  number of req docs, )
        # -- Write Output to files


     print(len(wl_list))
    for wlog in wl_list:
        print(" Weblog.ip : " + str(wlog.get_ip()) + "\n")