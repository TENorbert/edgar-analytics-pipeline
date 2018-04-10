#! python3


from datetime import datetime
from datetime import date
from datetime import time
from datetime import timedelta


def main():

    a = datetime.now()
    msg = "I don't give a f**k!"
    name = input("Whatz ur Name? ")
    print(name + "!" + msg)    
    b = datetime.now()
    duration = abs(a - b)
    time_elapse_in_s = duration.seconds
     
    print("The Elapse Time = {} s".format(time_elapse_in_s))


if __name__ == '__main__':
   
    main()
