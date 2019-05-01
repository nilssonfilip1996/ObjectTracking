# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 13:30:51 2019

@author: nilss
"""

import threading
import queue
import time
from pymongo import MongoClient
import json
             
class worker(threading.Thread):
    def __init__(self, name, stopper):
        threading.Thread.__init__(self)
        self._queue = queue.Queue(maxsize=0)
        self.name = name                    #Thread name
        self.stopper = stopper
        
    def run(self):
        print ("Starting " + self.name)
        while not self.stopper.is_set():
            time.sleep(1)
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
        Add functionality here:
            Step 1:
                Format the contenttuple to appropriate format that should be sent to connected clients.
            Step 2:
                Broadcast the formated data to ALL connected clients.
            Step 3:
                Done.
        """
        
#    def processContent(self, contenttuple):
#        print(contenttuple)
#        eventType = contenttuple[0]
#        if(eventType=='change'):
#            aDict = createChangeDict(contenttuple)
#            logToDB(aDict)
#        else:
#            eventList = contenttuple[2]
#            for e in eventList:
#                aDict = createAddOrRemoveDict(eventType,e)
#                logToDB(aDict)
    
#def writeToFile(fileName, content):
#    f = open(fileName, "a")
#    f.write(content)
#    f.close()
#    
#    
#def createChangeDict(contenttuple):
#    eventList = contenttuple[2]
#    markerId = contenttuple[1][0] #Only used for change event
#    prevCoord = eventList[0]
#    currCoord = eventList[1]
#    aDict = {'event':'change', 
#             'id' : markerId,
#             'previousLocation': {'x':prevCoord[0],'y':prevCoord[1]},
#             'currentLocation': {'x':currCoord[0],'y':currCoord[1]}}
#    return aDict
#
#def createAddOrRemoveDict(eventType, event):
#    markerId = event[0]
#    coord = event[1]
#    aDict = {'event': eventType,
#             'id':markerId,
#             'currentLocation': {'x':coord[0],'y':coord[1]}}
#    return aDict
#        
#
#"""
#Connect to mongoDB server.
#Cluster name: testcluster
#Database name: test
#Collection name: markerdata
#"""
#def logToDB(dictContent):
#    client = MongoClient("mongodb+srv://nilssonfilip:ekh9lMng@testcluster-m1vgd.gcp.mongodb.net/test?retryWrites=true")
#    db = client.get_database('test')
#    collection = db.get_collection('markerdata')
#    collection.insert_one(dictContent)

