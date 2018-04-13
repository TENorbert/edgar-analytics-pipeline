	#! python3
#  --- potentian solution


unique_weblogs = {}  # datetime dict with unique ip Address

weblog_queue = Q.priorityQueue()

prev_datetime = datetime.datetime.now() # use this for now


f_obj = open(filen_name, 'r')

lines = f_obj.readlines()
line_number = len(lines)  ## keep track of end of file

for  line in lines:
	line = line.strip()
	llist = line.split(',')

	ip = llist[0]
	cur_datetime = llist[1] + llist[2]
	req_doc = llist[4] + llist[5] + llist[6]
	#unique_weblogs[cur_datetime] = set() # keep only unique(ips) weblogs
	unique_weblogs[cur_datetime] = list() # As we might want to remove session ended weblogs from list

	#create weblog object
	cur_weblog = Weblog(ip, cur_datetime, cur_datetime, req_doc)

	## Now here is the LOGIC FLOW

if line != last_line:

# call_function(cur_weblog, prev_time, unique_weblogs, weblog_queue)
	if cur_weblog.start_datetime == prev_datetime:
		search_and_update_weblog(cur_weblog, unique_weblogs) 
		{ 

		#(better idea to use weblog n search in list of weblogs instead oflist of ip s?)
		if cur_weblog  IS NOT in unique_weblogs:  
		     then unique_weblogs[cur_datetime].add(cur_weblog)
		else:
		     update found weblog with new cur_weblog info

		     Goal: is to keep unique weblogs for each key(date_time)
		           and simply update a given weblog with new information(
		           end_datetime, number of requested document(count), duration(list))
		}

	else: # cur_datetime != prev_datetime
		elapse_time = get_elapse_time(prev_datetime, cur_datetime)
		if elapse_time < INACTIVITY_TIME: ##session isn't over yet
		   search_and_update_weblog(cur_weblog, unique_weblogs)
		elif elapse_time == INACTIVITY_TIME: #session ended
		    # return as list in case there are many weblogs with similar session ended
			 found_weblog_list = Search_and_return_found_weblog(cur_weblog, unique_weblogs) 
			 if len(found_weblog_list) != 0: #make sure we found something
			 	 Update_found_weblogs_info(cur_weblog, found_weblog_list)
			 	 Add_found_weblogs_to_Queue(found_web_log_list, weblog_queue)

	    elif elapse_time > INACTIVITY_TIME:




else: #reading last line
	call_function(cur_weblog, prev_time, unique_weblogs, weblog_queue)
	for weblog in unique_weblogs.values():
		weblog_queue.put(weblog)

f_obj.close() #close the file

# Now write results to file
write_results(weblog_queue)




def write_results(file_name, weblog_queue):
	'''
	   writes output from queue to output file_name
	'''
	while not weblog_queue.empty():
		wblog = weblog_queue.get()
		write_data_to_file(file_name, wblog.ip, wblog.start_datetime, wblog.end_datetime,
			wblog.get_number_req_doc, wblog.get_duration)




'''
def analyze(lines):
    '''
        #creates dictionary of weblogs for each line
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

'''