#! python3


from datetime import datetime
from datetime import date
from datetime import time
from datetime import timedelta

try:
    import Queue as Q # ver < 3.0
except ImportError:
    import queue as Q


def main():
    
    '''
    a = datetime.now()
    msg = "I don't give a f**k!"
    name = input("Whatz ur Name? ")
    print(name + "!" + msg)    
    b = datetime.now()
    duration = abs(a - b)
    time_elapse_in_s = duration.seconds
     
    print("The Elapse Time = {} s".format(time_elapse_in_s))
    '''
    myq = Q.Queue()
    
    doc = {'a': 1, 'b': 2, 'c': 1, 'd': 4}
    count = 0
    keys = ['a', 'b', 'c', 'd' ]
    for key in keys:
        count += doc[key]
        myq.put((key, doc[key]))
    print("Total Value in Dictionary = {}".format(count))
    
    while not myq.empty():
        next_level = myq.get()
        print("Processing item = {}".format(next_level))

if __name__ == '__main__':
   
    main()
