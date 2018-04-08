

import unittest



class VisitorActivity(object):
    """
      Takes ip_address(list), time(list), document(list) and creates
      produces session timeout time for each unqiue user(ip Address).
      Each Unique user is identified by a unique Ip Address
      All variables are read from a Weblog csv file
    """
    #def __init__(self, ifile, inacfile, ofile):
    def __init__(self):
        self.start_time = []  #list of time
        self.ip_address = []  #list of ip_address
        self.document_number = [] #list of document number


    def compute_elapsed_time(self):
        '''
            using start time, Ip adress, document generated
            it computes the session elapse time.
        '''
        print("Computing users Elapsed time!")
        pass

    def compute_inactivity(self):
        '''
           using number of request made by given user(ip address)
           computes the entire time during that activity( i.e user requesting 
           documents)
        '''
        print("Computing user's inactivity!")
        pass




class VisitorReport(object):
    '''
        Takes Elapsed Time, ip_address, Starttime, and Documents
        Requested to generate report stored in 
        sessionization.txt file.
    '''


    def generate_report(self):
        '''
           Generates the report which is continuously written to the
           sessionization file.
        '''
        # TO DO: Get Report and write report
        print("writing report!")
        pass