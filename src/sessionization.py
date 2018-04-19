

import unittest
from helper import *  # helper functions



def analyze(csv_filename, read_weblogs, output_weblogs ,inactivity_period):
    """
     creates dictionary of weblogs for each line and analyze each line!
    :param csv_filename:
    :param read_weblogs:
    :param output_weblogs:
    :param inactivity_period:
    :return:
    """
    try:
        data = read_csv(csv_filename)
        do_analysis(data, read_weblogs, output_weblogs, inactivity_period)

    except Exception as e:
        print(e, type(e))


def do_analysis(data, read_weblogs, output_weblogs, inactivity_period):
    """
    Perform Analysis and fills session ended weblogs in Queue
    Extract Outputs(ip, startTime, endtime, duration,  number of req docs) and
    Write Output to files
    :param data:
    :param read_weblogs:
    :param output_weblogs:
    :param inactivity_period:
    :return:
    """
    try:
        last_weblog = data[-1]
        #print(last_weblog)
        first_weblog = create_weblog(data[0])
        read_weblogs.append(first_weblog)
        #print("first Weblog has duration = {} s".format(first_weblog.duration))
        #print(first_weblog.ip_address)
        """
        if first_weblog.ip_address is not None:
        #read_weblogs.put(previous_weblog.start_datetime, previous_weblog)
        read_weblogs.put(first_weblog)
        #read_weblogs[first_weblog.start_datetime].append(first_weblog)
        """

        for i in range(1, len(data)):
            assert (len(data[i]) == 15 and len(last_weblog) == 15), "missing lines!"
            previous_weblog = create_weblog(data[i-1])
            current_weblog = create_weblog(data[i])

            #elapsed_time = get_elapse_time(previous_weblog.start_datetime, current_weblog.start_datetime)
            #print("Elapsed Time = {0}".format(elapsed_time))

            if data[i] is not last_weblog:
                #Analyze each weblog & update Queue

                analyze_and_update(current_weblog, previous_weblog,
                                   read_weblogs,
                                   output_weblogs,
                                   inactivity_period
                                   )
            else:
                #Analyze each weblog, update found weblogs & add weblogs to Queue

                analyze_and_update(current_weblog, previous_weblog,
                                   read_weblogs,
                                   output_weblogs,
                                   inactivity_period
                                   )

                finaly_update_priority_queue(read_weblogs, output_weblogs)

    except Exception:
        print("Function do_analysis failed!")


def analyze_and_update(cur_weblog, prev_weblog, read_weblogs, output_weblogs, period ):
    """
     Analyze current weblog with previous weblog and perform the needed action: weither add
     to list of weblogs or put into Queue
    :param cur_weblog:
    :param prev_weblog:
    :param read_weblogs:
    :param output_weblogs:
    :param period:
    :return:
    """
    try:

        if cur_weblog.start_datetime != prev_weblog.start_datetime: # change in date time so loop
            find_and_udate_or_add_weblog_to_weblogs(cur_weblog, read_weblogs, output_weblogs, period)
        else:
            update_weblog_and_add_to_priority_weblogs(cur_weblog, read_weblogs, output_weblogs, period)
    except Exception as e:
        print(e, type(e))

def find_and_udate_or_add_weblog_to_weblogs(c_weblog, read_weblogs, output_weblogs, period):
    """
    Search for current_weblog in the list and if already in list of weblogs, update its information(
    documents, duration etc) and if not add current weblog into list of weblogs.
    :param c_weblog:
    :param read_weblogs:
    :param output_weblogs:
    :param period:
    :return:
    """
    try:

        read_weblogs_ips = [] # go around non-iterable Aabstract class!
        for wlg in read_weblogs:
            read_weblogs_ips.append(wlg.ip_address)

        if c_weblog.ip_address not in read_weblogs_ips:
            add_to_weblogs(c_weblog, read_weblogs)
        else: # weblog already exist so?
            for cur_weblog in read_weblogs:
                elapse_time = get_elapse_time(cur_weblog.start_datetime, c_weblog.start_datetime)
                if elapse_time == period:
                    update_weblog_and_add_to_priority_weblogs(cur_weblog, read_weblogs, output_weblogs,period)
                else:
                    update_weblog(c_weblog, read_weblogs)
    except Exception as e:
        print(e, type(e))


def add_to_weblogs(c_weblog, read_weblogs):
    """
     Add new weblog created into the list of weblogs
    :param c_weblog:
    :param read_weblogs:
    :return:
    """
    try:

        read_weblogs_ips = []  #create possibly sorted list
        for wlg in read_weblogs:
            read_weblogs_ips.append(wlg.ip_address)

        if c_weblog.ip_address not in read_weblogs_ips:
            #print("Adding ip = {0} & document = {1} to Weblogs!".format(c_weblog.ip_address, c_weblog.request_document))
            read_weblogs.append(c_weblog)
        else:
            pass
    except Exception as e:
        print(e, type(e))



def update_weblog(c_weblog, read_weblogs):
    """
     Updates found weblog i.e if current weblog( ip address) already in list with current weblog
     document and duration.
    :param c_weblog:
    :param read_weblogs:
    :return:
    """
    try:
        if len(read_weblogs) == 0:
            add_to_weblogs(c_weblog, read_weblogs)

        for cur_weblog in read_weblogs:
            if cur_weblog.has_same_ip(c_weblog):
                if cur_weblog.has_same_start_datetime(c_weblog): #??
                    if cur_weblog.request_document != c_weblog.request_document:
                        cur_weblog.update_weblog_with_other(c_weblog)
            else:
                if cur_weblog.has_same_start_datetime(c_weblog):  #??
                    add_to_weblogs(c_weblog, read_weblogs)
    except Exception as e:
        print(e, type(e))

def update_weblog_and_add_to_priority_weblogs(c_weblog, read_weblogs, output_weblogs, priority):
    """
     Update found weblogs( if Ip address weblog already in list) and check if session as ended
     then put session ended weblogs into Queue.
    :param c_weblog:
    :param read_weblogs:
    :param output_weblogs:
    :param priority:
    :return:
    """
    try:

        for cur_weblog in read_weblogs:
            if cur_weblog.has_same_ip(c_weblog):
                cur_weblog.update_weblog_with_other(c_weblog)
                elapse_time = get_elapse_time(cur_weblog.start_datetime, c_weblog.start_datetime)
                if elapse_time == priority:
                    output_weblogs.put(cur_weblog)
            else: # Different IPs
                add_to_weblogs(c_weblog, read_weblogs)

                #remove cur_weblog from read_weblogs
                # To Do: How to remove element from Queue? or use Linked List
    except Exception as e:
        print(e, type(e))


def finaly_update_priority_queue(read_weblogs, output_weblogs):
    """
    Supposed to transfer remaining session-yet-to-end weblogs into Queue ordered in date time
    as read from file into the Queue.
    Tried using a PriorityQueue with read date time as priority but ran into so many debugging
    issues. Will be fun to get this going!
    :param read_weblogs:
    :param output_weblogs:
    :return:
    """
    try:
        output_weblog_ips = []
        while not output_weblogs.empty():
            webg = output_weblogs.get()
            output_weblog_ips.append(webg.ip_address)

        # TO Do: Put in some entry/read priority?
        if len(read_weblogs) != 0:
            for weblog in read_weblogs:
                if weblog.ip_address in output_weblog_ips:
                    continue
                else:
                    output_weblogs.put(weblog)
                    #pass  # need to update end_datetime, duration & number of documents!
    except Exception as e:
        print(e, type(e))

    """
    if len(read_weblogs) != 0:
    for i in range(len(read_weblogs)):
        output_weblogs.put(read_weblogs[i])  # TO Do: Put in some entry/read priority?
    """

def write_output(output_queue, file_name):
    """
    Takes given data in output_queue and writes(append each time) the data to txt file
    Default file path is '..'

    :param file_name:
    :param output_container:
    :return:
    """
    try:
        with open(file_name, 'a') as f_obj:
            f_obj.write("Output_weblogs length = {0}".format(output_queue.qsize()))
            '''
            while not output_queue.empty():
                cur_weblog = output_queue.get()
                f_obj.write(str(cur_weblog.ip_address) + ',' + str(cur_weblog.start_datetime) + ','
                           + str(cur_weblog.end_datetime) + ',' + str(cur_weblog.request_document) + ','
                            + str(cur_weblog.duration) + ',' + str(cur_weblog.get_document_number()) + "\n"
                           )
            '''
    except Exception as e:
        print("FileNotFoundError")
        print(e, type(e))
        ##print("File Not found!")




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
        self.duration = 1  # the most recent weblog duration
        self.doc_number = 1  # Number of requested documents, a weblog created = first document requested

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
        if len(self.weblog_durations) != 0:
            return sum(self.weblog_durations)
        else:
            return self.duration
    """
    def get_document_count(self):
        '''
        Returns document number based on start_datetime?
        :param date_time_list:
        :return:
        '''
        count = 0
        for dt in self.requested_documents:
            count += self.document_counter[dt]  # Sum length of all date times for this ip
        return count
    """

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
            if len(self.requested_documents) != 0:
                self.doc_number = len(self.requested_documents)
            else:
                self.doc_number = 1  ## atlease one duration used must have been requested!


    def add_duration(self, end_datetime):
        '''

        :param end_datetime:
        :return:
        '''
        if self.end_datetime != end_datetime:  # found a new end_datetime
            self.end_datetime = end_datetime
            val = self.compute_duration()
            self.weblog_durations.append(val)
            if len(self.weblog_durations) != 0:
                self.duration = self.get_total_duration()
            else:
                self.duration = 1  ## atlease one duration used!
        else:
            self.duration = 1  ## atlease one duration used!

    ## Helper Functions
    def compute_duration(self):
        #start = datetime.strptime(self.start_datetime, '%Y-%m-%d:%H:%M:%S')
        #end = datetime.strptime(self.end_datetime, '%Y-%m-%d:%H:%M:%S')
        #val = get_elapse_time(end, start)
        val = get_elapse_time(self.start_datetime, self.end_datetime)
        default_val = 1
        if val == 0:
            self.weblog_durations.append(default_val)
        else:
            self.weblog_durations.append(val)

        self.duration = self.get_total_duration()

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
        self.compute_duration()
        self.add_duration(self.end_datetime)
        self.add_document(self.request_document)
        self.doc_number = len(self.requested_documents)

    def update_weblog_with_other(self, other):
        '''
         Updates the infomation of self with other
        :param other:
        :return:
        '''
        self.doc_number += 1
        self.end_datetime = other.start_datetime
        self.add_duration(other.end_datetime)
        self.compute_duration()
        self.add_document(other.request_document)
        self.doc_number = len(self.requested_documents)



##--------- Helper Functions ---------------------------------------------------------------------------
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


## ---- Unused Functions--------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------------
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



def update_same_ip_scenario(cur_weblog, read_weblogs):
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
        read_weblogs[cur_weblog[2]].append(cur_weblog)

    except Exception as e:
        print(e, type(e))

def update_different_ip_scenario(cur_weblog, read_weblogs):
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
        if cur_weblog[2] not in read_weblogs.keys():
            cur_weblog.append(end_datetime)
            #new key or date time so create field
            duration = get_elapse_time(cur_weblog[1], cur_weblog[3])
            cur_weblog.append(duration)
            weblog_req_docs.append(cur_weblog[2])
            num_req_doc = len(weblog_req_docs)
            cur_weblog.append(num_req_doc)

            read_weblogs[cur_weblog[2]].append(cur_weblog)
        else:
            print("Dupplicate Document request!")

    except Exception as e:
        print(e, type(e))

#==================================================================================================
#==================================================================================================
'''
    if prev_session[1] == cur_session[1] : # weblogs have same date time
    #if get_elapse_time(cur_session[1], prev_session[1]) == 0: # weblogs have same date time
        if cur_session[0] != prev_session[0]: #Different Ip as previous
            print("------------------------------------------------------------------")
            update_different_ip_scenario(cur_session, read_weblogs)
            print("Different IPs Weblogs")
            print("------------------------------------------------------------------")
        else: # Same Ip  as previous!
            print("------------------------------------------------------------------")
            update_same_ip_scenario(cur_session, read_weblogs)
            print("Same IPs Weblogs")
            print("------------------------------------------------------------------")

    else:
        elapsed_time = get_elapse_time(prev_session[1], cur_session[1])
        #print("Use Elapse time Comparison!")

        if elapsed_time < inactivity_period: #Session isn't over yet!
            if cur_session[0] == prev_session[0]: #same Ip as previous
                update_different_ip_scenario(cur_session, read_weblogs)
                print("elapsed time = {0}".format(elapsed_time))
            # TO DO:
            # search_and_update_output_weblogs(cur_session, read_weblogs)

        elif elapsed_time == inactivity_period: #session is over!
            print("elapsed time = {0}".format(elapsed_time))
            # To DO:
            # Search_and_return_found_weblog(cur_session, read_weblogs)
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


#output_weblogs.put((q_priority, cur_session))
#wl = Weblog(ip_adr, dt_obj, dt_obj, req_doc)
#output_weblogs.put((q_priority, wl))
#print(" Weblog.ip : " + str(wl.get_ip()) + "\n")
print("Total found Weblogs = {0} \n".format(len(read_weblogs)))
if len(read_weblogs) != 0:
    for key, web_logs in read_weblogs.items():
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



