# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 13:30:51 2019

@author: nilss
"""

import threading

class eventHandler(threading.Thread):
    
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name                    #Thread name
        self._queue = []
    
    def run(self):
      print ("Starting " + self.name)
      for i in range(5):
          print(i)
      print ("Exiting " + self.name)
      
    def enQueue(self, li):
        self._queue.append(li)
        print("-----------")
        for i in self._queue:
            print(i)
        print("-----------")

