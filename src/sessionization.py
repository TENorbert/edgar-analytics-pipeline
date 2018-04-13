

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
        data = read_csv(csv_filename)
        do_analysis(data, weblog_queue, inactivity_period)

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




def do_analysis(data, weblog_queue, inactivity_period):
    '''
        Performs the analysis
    '''
    #weblog_elements = Q.PriorityQueue() # Testing using PQueues
    weblog_elements = Q.Queue()  # Testing using PQueues
    #cur_session = []
    #prev_session = [] #previous weblog
    found_weblogs = {} #found weblogs(key = start_time, values = rows)
    last_weblog = data[-1]
    #print(last_weblog)
    #prev_session = create_session(data[0])
    first_weblog = create_weblog(data[0])
    #found_weblogs[first_weblog.start_datetime] = []
    #if len(prev_session) != 0:
    if first_weblog.ip_address != None:
        #found_weblogs[str(prev_session[1])] = [] #list of weblogs
        #found_weblogs[prev_session[1]].append(prev_session)
        #print("Created First Weblog and added to Dictionary!")
        #print(found_weblogs[prev_session[1]][0])
        #weblog_elements.put(previous_weblog.start_datetime, previous_weblog)
        weblog_elements.put(first_weblog)
        #found_weblogs[first_weblog.start_datetime].append(first_weblog)

    for i in range(1, len(data)):
        assert (len(data[i]) == 15 and len(last_weblog) == 15), "missing lines!"
        #prev_session = create_session(data[i-1])
        #cur_session = create_session(data[i])
        previous_weblog = create_weblog(data[i-1])
        current_weblog = create_weblog(data[i])

        if data[i] is not last_weblog:
            #weblog_elements.put(current_weblog.start_datetime, current_weblog)
            weblog_elements.put(current_weblog)
            #found_weblogs[current_weblog.start_datetime].append(current_weblog)

            # To Do
            # Analyze
            # update Priority Queue

        else:
            weblog_elements.put(current_weblog)
            #found_weblogs[current_weblog.start_datetime].append(current_weblog)
            # To Do
            # Analyze
            # Add all elements to Priority Queue







        # To Do:
        # Write Queue Data to Output file


        while not weblog_elements.empty():
            cur_weblog = weblog_elements.get()
            #print(cur_weblog)
            print("{0}, {1}, {2}, {3}, {4}, {5} \
                        ".format(cur_weblog.ip_address, cur_weblog.start_datetime,
                                 cur_weblog.end_datetime, cur_weblog.request_document,
                                 cur_weblog.duration, cur_weblog.doc_number)
                      )
            #print("key = {} and Weblog_document = {}".format(key, value.start_datetime ))


        """
        for key, web_logs in found_weblogs.items():
            # print("found Weblogs \n")
            print("key = {0} has {1} Weblogs".format(key, len(web_logs)))
            print("======================================================================")
            for _wlog in found_weblogs[key]:
                # print("_wlog Length = {0}".format(len(_wlog)))
                print("{0}, {1}, {2}, {3}, {4}, {5} \
                        ".format(_wlog.ip_address, _wlog.start_datetime,
                                 _wlog.end_datetime, _wlog.request_document,
                                 _wlog.duration, _wlog.doc_number)
                      )

                #print("{0}, {1}, {2} \
                #".format(_wlog.ip_address, _wlog.start_datetime, _wlog.request_document))
        """


        '''
        if prev_session[1] == cur_session[1] : # weblogs have same date time
        #if get_elapse_time(cur_session[1], prev_session[1]) == 0: # weblogs have same date time
            if cur_session[0] != prev_session[0]: #Different Ip as previous
                print("------------------------------------------------------------------")
                update_different_ip_scenario(cur_session, found_weblogs)
                print("Different IPs Weblogs")
                print("------------------------------------------------------------------")
            else: # Same Ip  as previous!
                print("------------------------------------------------------------------")
                update_same_ip_scenario(cur_session, found_weblogs)
                print("Same IPs Weblogs")
                print("------------------------------------------------------------------")
                
        else:
            elapsed_time = get_elapse_time(prev_session[1], cur_session[1])
            #print("Use Elapse time Comparison!")

            if elapsed_time < inactivity_period: #Session isn't over yet!
                if cur_session[0] == prev_session[0]: #same Ip as previous
                    update_different_ip_scenario(cur_session, found_weblogs)
                    print("elapsed time = {0}".format(elapsed_time))
                # TO DO:
                # search_and_update_weblog_queue(cur_session, found_weblogs)

            elif elapsed_time == inactivity_period: #session is over!
                print("elapsed time = {0}".format(elapsed_time))
                # To DO:
                # Search_and_return_found_weblog(cur_session, found_weblogs)
                # Add found weblog to priority Queue

            else: #elapse_time_is_greater!
                print("elapsed time = {0}".format(elapsed_time))
                ## TO DO:
                #  Handle greater then elapse time

    else: # Handle last weblog
        pass
        # TO DO
        # Handle Scenrio of last line read

    #print("Previous session ip = {}\n".format(prev_session[0]))
    #print("current session ip = {}\n".format(cur_session[0]))


    #weblog_queue.put((q_priority, cur_session))
    #wl = Weblog(ip_adr, dt_obj, dt_obj, req_doc)
    #weblog_queue.put((q_priority, wl))
    #print(" Weblog.ip : " + str(wl.get_ip()) + "\n")
    print("Total found Weblogs = {0} \n".format(len(found_weblogs)))
    if len(found_weblogs) != 0:
        for key, web_logs in found_weblogs.items():
            #print("found Weblogs \n")
            #print("Web log lenth = {}".format(len(web_logs)))
            print(key)
            print("======================================================================")
            for _wlog in web_logs:
                #print("_wlog Length = {0}".format(len(_wlog)))
                if len(_wlog) == 6:
                    print("{0}, {1}, {2}, {3}, {4}, {5} \
                    ".format(_wlog[0], _wlog[1], _wlog[2], _wlog[3], _wlog[4], _wlog[5]))
                #else:
                #    print("{0}, {1}, {2} \
                #    ".format(_wlog[0], _wlog[1], _wlog[2]))
        '''


class Weblog(object):
    """
      Takes ip_address, dateTime, document and creates a weblog(session) Object
      session timeout time for each unqiue user(ip Address).
      Each unique user(or weblog) is identified by a unique Ip Address
    """

    def __init__(self, ip_address, start_datetime, end_datetime, request_document):
        self.ip_address = ip_address
        self.start_datetime = start_datetime  # Use start_datetime as priority
        self.end_datetime = end_datetime
        self.request_document = request_document
        self.requested_documents = []  # list of requested documents
        self.document_counter = {}  # Dictionary of state_date_time(key) and number of requested documents(values)
        self.weblog_durations = [] # list of all durations in this weblog
        self.duration = 0  # the most recent weblog duration
        self.doc_number = 0  # Number of requested documents

        self.update_weblog_info() ## update additional weblog info

    def __cmp__(self, other):
        return cmp(self.start_datetime, other.start_datetime)

    # Acessors/Getters
    def get_ip(self):
        return self.ip_address

    def get_start_datetime(self):
        return self.start_datetime

    def get_end_datetime(self):
        return self.end_datetime

    def get_request_document(self):
        return self.request_document

    def get_duration(self):
        return self.duration

    def get_document_number(self):
        return len(self.requested_documents)

    def get_total_duration(self):
        return sum(self.weblog_durations)

    def get_document_count(self, date_time_list):
        '''
            Returns document number based on start_datetime?
        :param date_time_list:
        :return:
        '''
        count = 0
        for dt in date_time_list:
            count += self.document_counter[dt]  # Sum length of all date times for this ip
        return count

    # M Mutators/Setters
    def set_ip(self, ip_address):
        self.ip_address = ip_address  ## Not needed ? Why change  the IP?

    # TO DO!!
    # each time we change the start & endtime for a same ip_adress
    # shouldn't we just updated the doc request and duration?
    def set_start_datetime(self, start_datetime):
        self.state_date_time = start_datetime

    def set_end_datetime(self, end_datetime):
        self.set_end_datetime = end_datetime

    def set_request_document(self, req_doc):
        self.request_document = req_doc

    def set_duration(self, duration):
        self.duration = duration

    def set_document_count(self, date_time):
        self.document_counter[date_time] = 1

    def add_document(self, req_document):
        '''
        Add requested document to document list
        :param req_document:
        :return:
        '''
        if req_document not in self.requested_documents:
            self.requested_documents.append(req_document)

    def add_duration(self, end_datetime):
        if self.end_datetime != end_datetime:  # found a new end_datetime
            self.end_datetime = end_datetime
            val = self.compute_duration()
            self.weblog_durations.append(val)

    ## Helper Functions
    def compute_duration(self):
        #start = datetime.strptime(self.start_datetime, '%Y-%m-%d:%H:%M:%S')
        #end = datetime.strptime(self.end_datetime, '%Y-%m-%d:%H:%M:%S')
        #val = get_elapse_time(end, start)
        val = get_elapse_time(self.start_datetime, self.end_datetime)
        self.duration = val

    def has_same_ip(self, other):
        '''
        checks if two web logs have same ip
        :param other:
        :return: True/False
        '''
        return (self.ip_address == other.ip_address)

    def has_same_start_datetime(self, other):
        '''
          Takes a weblog and checks if it has the same start_datetime as self.
        :param other:
        :return: True/False
        '''
        return (self.start_datetime == other.start_datetime)


    def update_weblog_info(self):
        '''
        Called on __init__ method to update weblog information
        :return:
        '''
        self.add_duration(self.end_datetime)
        self.compute_duration()
        self.add_document(self.request_document)
        self.doc_number = len(self.requested_documents)


def create_weblog(row):
    '''
    creates a weblog object:
    weblog from row : list[0] = ip_address
                      list[1] = date_time
                      list[2] = requested_document
    :param row:
    :return:
    '''

    wlg_ip = row[0]
    wlg_datetime = create_date_time(row[1], row[2])
    wlg_document = create_request_document(row[4], row[5], row[6])
    weblog = Weblog(wlg_ip, wlg_datetime, wlg_datetime, wlg_document)

    return weblog


def create_session(row):
    '''
        Uses row from file to create a given session:
         A given Session = ip_address, date + time, cik + accession + extension

        Returns : session as a list[0] = ip_address
                               list[1] = date_time
                               list[2] = requested_document
    '''
    sess_elements = []  # contents of a given session
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



def update_same_ip_scenario(cur_weblog, found_weblogs):
    '''
    '''
    weblog_req_docs = [] # list of requested documents
    end_datetime = cur_weblog[1]
    weblog_dur = 0
    num_req_doc = 0

    try:
        cur_weblog.append(end_datetime) #add end_time to session weblog
        weblog_dur = get_elapse_time(cur_weblog[1], cur_weblog[3])
        cur_weblog.append(weblog_dur) # add duration to session weblog
        weblog_req_docs.append(cur_weblog[2]) # add document to list
        num_req_doc = len(weblog_req_docs)   
        cur_weblog.append(num_req_doc) # update # of documents for session
        found_weblogs[cur_weblog[2]].append(cur_weblog)

    except Exception as e:
        print(e, type(e))





def update_different_ip_scenario(cur_weblog, found_weblogs):
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
    end_datetime = cur_weblog[1]
    duration = 0
    num_req_doc = 0
    try:
        if cur_weblog[2] not in found_weblogs.keys():
            cur_weblog.append(end_datetime)
            #new key or date time so create field
            duration = get_elapse_time(cur_weblog[1], cur_weblog[3])
            cur_weblog.append(duration)
            weblog_req_docs.append(cur_weblog[2])
            num_req_doc = len(weblog_req_docs)
            cur_weblog.append(num_req_doc)

            found_weblogs[cur_weblog[2]].append(cur_weblog)
        else:
            print("Dupplicate Document request!")

    except Exception as e:
        print(e, type(e))





