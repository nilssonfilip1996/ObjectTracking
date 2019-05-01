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
        
    def run(self):
        print ("Starting " + self.name)
        while not self.stopper.is_set():
            time.sleep(0.5)
            res = self.deQueue()
            if(res!=None):
                print("Work found!")
                self.processContent(res)
        print ("Exiting " + self.name)
        
    def enQueue(self, li):
        self._queue.put(li)
    
    def deQueue(self):
        if(not self._queue.empty()):
            val = self._queue.get()
            self._queue.task_done()
            return val
        else:
            return None
        
    def processContent(self, contentDict):
        print(contentDict)
        """
        Add API functionality here:
            Step 1:
                Broadcast the formated data to ALL connected clients.
            Step 2:
                Done.
        """

