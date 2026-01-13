# Source - https://stackoverflow.com/q
# Posted by user416384, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-28, License - CC BY-SA 2.5

import threading
import time
import random
#the list "data" must contain two values.  
#The second must always be equal to the first multiplied by 4

class GeneratorThread(threading.Thread):
    #Thread for generating value pairs
    def __init__(self,data):
        threading.Thread.__init__(self)
        self.data=data
    def run(self):
        while True:
            #Pick a new first number
            num=random.randint(0,100)
            self.data[0]=num
            #simulate some processing 
          #to calculate second number
            time.sleep(1)
            #Place second value into ata
            self.data[1]=num*4
            time.sleep(1)
class ProcessorThread(threading.Thread):
    #Thread for processing value pairs
    def __init__(self,data):
        threading.Thread.__init__(self)
        self.data=data
    def run(self):
        while True:
            #Process current data
            num1=self.data[0]
            num2=self.data[1]
            print ("Values are %d and %d."%(num1,num2))
            if num2!=num1*4:
                print ("\tDATA INCONSISTENCY!")
            time.sleep(2)
if __name__=="__main__":
    data=[1,4]
    t1=GeneratorThread(data)
    t2=ProcessorThread(data)
    t1.start()
    t2.start()
