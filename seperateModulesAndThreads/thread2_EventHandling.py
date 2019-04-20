# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 13:30:51 2019

@author: nilss
"""

import threading
import queue
import time
             
class worker(threading.Thread):
    def __init__(self, name, stopper):
        threading.Thread.__init__(self)
        self._queue = queue.Queue(maxsize=0)
        self.name = name                    #Thread name
        self.stopper = stopper
        #self.eventHandler = eh
        
    def run(self):
        print ("Starting " + self.name)
        while not self.stopper.is_set():
        #while True:
            time.sleep(1)
            #print("hej")
            res = self.deQueue()
            if(res!=None):
                print("Work found!")
                print(res)
                self.processContent(res)
        print ("Exiting " + self.name)
        
    def enQueue(self, li):
        self._queue.put(li)
        #self._queue.task_done()
        #print(self._queue.qsize())
    
    def deQueue(self):
        #print("hey")
        if(not self._queue.empty()):
            val = self._queue.get()
            self._queue.task_done()
            return val
        else:
            return None
        
    def processContent(self, contenttuple):
        eventType = contenttuple[0]
        eventList = contenttuple[2]
        if(eventType=='change'):
            markerId = contenttuple[1][0] #Only used for change event
            eStr = eventType + " " + str(markerId) + " " + str(eventList) + "\n"
        else:
            eStr = ""
            for e in eventList:
                eStr += eventType + " " + str(e[0]) + " " + str(e[1]) + "\n"
        writeToFile("testFile.txt", eStr)
    
def writeToFile(fileName, content):
    f = open(fileName, "a")
    f.write(content)
    f.close()

