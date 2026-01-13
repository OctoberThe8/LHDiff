# Source - https://stackoverflow.com/a
# Posted by paxdiablo, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-28, License - CC BY-SA 2.5

#!/usr/bin/python

import threading
import time
import random
#the list "data" must contain two values.
#The second must always be equal to the first multiplied by 4

# declare the mutex so the snippet is minimally self-contained
datamutex = threading.Lock()

class GeneratorThread(threading.Thread):
    #Thread for generating value pairs
    def __init__(self,data):
        threading.Thread.__init__(self)
        self.datamutex=datamutex         # save reference to the mutex.
        self.data=data
    def run(self):
        while True:
            #Pick a new first number
            num=random.randint(0,100)
            self.datamutex.acquire()     # get the mutex.
            self.data[0]=num
            #simulate some processing
          #to calculate second number
            time.sleep(1)
            #Place second value into ata
            self.data[1]=num*4
            self.datamutex.release()     # release it to allow other thread
                                         #  to run now that data is consistent.
            time.sleep(1)

class ProcessorThread(threading.Thread):
    def __init__(self, data):
        threading.Thread.__init__(self)
        self.datamutex = datamutex
        self.data = data
    def run(self):
        while True:
            self.datamutex.acquire()
            num1 = self.data[0]
            num2 = self.data[1]
            print("Values are %d and %d." % (num1, num2))
            self.datamutex.release()
            if num2 != num1 * 4:
                print("\tDATA INCONSISTENCY!")
            time.sleep(2)

if __name__ == "__main__":
    data = [1, 4]
    t1 = GeneratorThread(data)
    t2 = ProcessorThread(data)
    t1.start()
    t2.start()