#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

    This class contains the worker. The worker
    handles an event queue. Events are sent
    to the queque asynchronously from two camera
    feeds. Once received by the worker they are
    stored and passed on to an MQTT broker.
    
    @author: Aron Polner & Filip Nilsson 9/5/2019

"""

import threading
import queue
import time

import json
             
class worker(threading.Thread):
    def __init__(self, name, stopper, client):
        threading.Thread.__init__(self)
        self._queue = queue.Queue(maxsize=0)
        self.name = name                    #Thread name
        self.stopper = stopper
        self.mqttClient = client
        
    def run(self):
        print ("Starting " + self.name)
        self.processContent({"start":"start"})
        while not self.stopper.is_set() or not self._queue.empty():
            res = self.deQueue()
            if(res!=None):
                self.processContent(res)
            time.sleep(0.1)
        self.processContent({"end":"end"})
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
        data_out=json.dumps(contentDict) # json.loads - decodes json into a python object 
        self.mqttClient.publish("tracking_data", data_out)
        

