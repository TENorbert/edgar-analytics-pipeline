

import unittest
from helper import *  # helper functions

try:
    import Queue as Q # ver. < 3.0
except ImportError:
    import queue as Q





'''
ip_list.append(split_line[0])
date_list.append(split_line[1])
time_list.append(split_line[2])
cik_list.append(split_line[4])
acession_list.append(split_line[5])
ext_list.append(split_line[6])
'''


def analyze(csv_filename, inactivity_period):
    '''
        creates dictionary of weblogs for each line
    '''
    weblog_queue = Q.PriorityQueue() ## scalability
    wl_number = 0 ## use as priority
    try:
        #print(get_last_row(csv_filename)) # buffer size must be interger <class, TypeErro>
        csv_fobj = open(csv_filename)
        #last_row = csv_fobj.readlines()[-1]  ## Last Row
        readobj = csv.reader(csv_fobj)
        for row in readobj:
            row_num = readobj.line_num
            if row_num == 1: ## Skip title line
                continue

            

            #print(last_row)
            do_analysis(row, row_num, weblog_queue, inactivity_period)

    except Exception as e:
        print(e, type(e))

    """
    while not weblog_queue.empty():
        key, wlog = weblog_queue.get()
        #print("key : " + str(key) + " Weblog.ip : " + str(wlog.get_ip()) + "\n")
        print("key : " + str(key) + " Weblog IP = : " + str(wlog[0] + "\n"))
    """
        #TO DO:
        # -- Perform Analysis()
        # -- Extract Outputs(ip, startTime, endtime, duration,  number of req docs, )
        # -- Write Output to files







def do_analysis(row, q_priority, weblog_queue, inactivity_period):
    '''
        Performs the analysis
    '''
    cur_session = [] 
    prev_session = []  #previous_session

    found_weblogs = {} #found weblogs(key = date_time, values = rows)
    if len(row) == 15:

        cur_session = create_session(row)

        if len(prev_session) == 0:# first read weblog
            found_weblogs[cur_session[1]] = list() # unique list of list of weblogs
            #found_weblogs[cur_session[1]].append(cur_session)
            print("empty Prev_weblog")
        else:

            print("Not Empty Prev_weblog")
            '''
            if cur_session[1] == prev_session[1]: # weblogs have same date time
            #if get_elapse_time(cur_session[1], prev_session[1]) == 0: # weblogs have same date time
     
                if cur_session[0] == prev_session[0]: #same Ip as previous
                    find_and_update_found_weblog(cur_session, found_weblogs)
                    print("Same IPs Weblogs")
            else:
                elapsed_time = get_elapse_time(prev_session[1], cur_session[1])
                #print("Use Elapse time Comparison!")

                if elapsed_time < inactivity_period: #Session isn't over yet!
                    print("elapsed time = ".format(elapsed_time))
                    # TO DO:
                    # search_and_update_weblog_queue(cur_session, found_weblogs)

                elif elapsed_time == inactivity_period: #session is over!
                    print("elapsed time = ".format(elapsed_time))
                    # To DO:
                    # Search_and_return_found_weblog(cur_session, found_weblogs)
                    # Add found weblog to priority Queue

                else: #elapse_time_is_greater!
                    print("elapsed time = ".format(elapsed_time))
                    ## TO DO:
                    #  Handle greater then elapse time

            '''
        # update prev_session to current_session
        #print("current session ip = {}\n".format(cur_session[0]))
        #prev_session = cur_session[:] # assign a copy!
        #print("Previous session ip = {}\n".format(prev_session[0]))






        #weblog_queue.put((q_priority, cur_session))
        #wl = Weblog(ip_adr, dt_obj, dt_obj, req_doc)
        #weblog_queue.put((q_priority, wl))
        #print(" Weblog.ip : " + str(wl.get_ip()) + "\n")

        if len(found_weblogs) != 0:
            for date_time, web_logs in found_weblogs.items():
                #print("found Weblogs \n")
                #print("Web log lenth = {}".format(len(web_logs)))
                print("date time = {0} , weblogs = {1}".format(date_time, web_logs))
                #for _wlog in web_logs:
                #    if len(_wlog) == 6:
                #        print("{0}, {1}, {2}, {3}, {4}, {5} \
                #        ".format(_wlog[0], _wlog[1], _wlog[2], _wlog[3], _wlog[4], _wlog[5]))
                #    else:
                #        print("{0}, {1}, {2} \
                #        ".format(_wlog[0], _wlog[1], _wlog[2]))
        




def create_session(row):
    '''
        Uses row from file to create a given session: 
         A given Session = ip_address, date + time, cik + accession + extension

        Returns : session as a list[0] = ip_address
                               list[1] = date_time
                               list[2] = requested_document
    '''
    sess_elements = [] # contents of a given session
    try:
        sess_ip = row[0]
        sess_datetime = create_date_time(row[1], row[2])
        sess_document = create_request_document(row[4], row[5], row[6])
        sess_elements.append(sess_ip)
        sess_elements.append(sess_datetime)
        sess_elements.append(sess_document)
    except Exception as e:
        print(e, type(e))
    return sess_elements




def find_and_update_found_weblog(cur_weblog, found_weblogs):
    '''
        Takes current weblog and searches for current weblog in found weblogs and 
        searches using ip address if current weblog has already been found and then
        adds end_datetime, current duration, and number of documents requested.
        weblog[0] = ip_address
        weblog[1] = start_datetime(date + time)
        weblog[2] = requested Document(cik + accession + extention)
        weblog[3] = end_datetime((date + time))
        weblog[4] = duration
        weblog[5] = Number of Requested Documents 
        ... coud add list of requested documents
    '''
    weblog_req_docs = [] # list of requested documents
    try:
        for date_time, weblogs in found_weblogs.items():
            if date_time == cur_weblog[1]: #found the current session date time
                for weblog in weblogs:
                    if cur_weblog[0] == weblog[0]: #found session with current ip
                        duration = get_elapse_time(weblog[1], cur_weblog[1])
                        weblog.append(cur_weblog[1]) #add end_time to session weblog
                        weblog.append(duration) # add suration to session weblog
                        if cur_weblog[2] != weblog[2]: # new requested document
                            weblog_req_docs.append(cur_weblog[2]) # add document to list
                        weblog.append(len(weblog_req_docs)) # update # of documents for session

    except Exception as e:
        print(e, type(e))







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
