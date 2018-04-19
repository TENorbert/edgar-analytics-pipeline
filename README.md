# Edgar Analytics
See analytics problem challenge here:
https://github.com/InsightDataScience/edgar-analytics


# First attempt at solution to Problem
-1. Use OOP approach by treating each weblog as a class object.
-2. Use List(or Dictionary) to keep track of read weblogs(each line in file)
-3. Use Queue to keep track of session ended weblogs( first in first out)
-4. As weblogs are read from file, each time there is a change in date time read, go through
already read weblogs in list and either update their number of documents, durations
for those with same Ip addresses already existing in list or create and add new Ip address
for the current weblog(line) being read into the list
-5. If the current line read from file is the last line, then repeat above step 4 and add all those
remaining weblogs whose sessions are yet to end into the Queue according to date time read from file.
-6. Print/save contents of Queue into the screen/outputfile

# Solution Implementation
    class Weblog(object)
    {
        ** properties **
        * 'ip address':
        * 'start date time':
        * 'end date time':
        * 'duration': latest duration for this weblog, default is 1 once weblog is first created
        * 'duration list': list of durations for this weblog
        * 'requested document': Latest document requested by this(ip address) weblog
        * 'requested document list': list of requested documents by this weblog

        ** Methods **
        * Accessors
        * Mutators
        * Helper functions
    }

    Function to perform the counting and updating analysis
    ** ##do_analysis(data, read_weblogs, output_weblogs, inactivity_period)
       -- ## analyze_and_update(cur_weblog, prev_weblog, read_weblogs, output_weblogs, period ):
    Writing the session ended weblogs in some priority of session ended date time and start datetime or as
    read from the input file.

# Solution Testing
Apart from single unit testing and use of defensive program try ... except,
I have not really developed and run any full testing on this entire code.
 ### TO DO:
* Write a full unit and integration test
* Use better data structures.
Still work to do.

# Improvement
 * Solution not working as expected at the moment, still need more time to adjust solution.
 * Check posible performance improvement and better logic.
 * Use dictiornary or linked list instead of list to keep track of weblogs(lines from input file) read.
 * Test possible solution scenario.
 * Find other better solutions.
