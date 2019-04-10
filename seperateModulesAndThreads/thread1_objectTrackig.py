#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 13:37:35 2019

@author: orgel & Filip
"""

#from __future__ import print_function
import urllib
import cv2
from ar_markers import detect_markers
import threading
import numpy as np
import time


class imageFeed(threading.Thread):
    def __init__(self, url, name):
        threading.Thread.__init__(self)
        self.url = url
        self.name = name
        #self.start()
        
    def run(self):
      print ("Starting " + self.name)
      self.stream()
      print ("Exiting " + self.name)
        
    def stream(self):
        print('Press "q" to quit')
        while True:
            #time.sleep(0.1) #Delay for easier console reading
            frame = self.getMobileFrame(self.url)
            markers = detect_markers(frame)
            print(markers)
            frame = cv2.resize(frame, (1210,720))
            cv2.imshow('Detection Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
        cv2.destroyAllWindows()
        
    
    
    def getMobileFrame(self, url):
        # Use urllib to get the image from the IP camera
        imgResp = urllib.request.urlopen(url)
        # Numpy to convert into a array
        imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
        # Finally decode the array to OpenCV usable format
        return cv2.imdecode(imgNp,-1)
    
    

class myThread (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
      
   def run(self):
      print ("Starting " + self.name)
      print_time(self.name, self.counter, 10)
      print ("Exiting " + self.name)

def print_time(threadName, delay, counter):
   while counter:
      time.sleep(delay)
      print ("%s: %s" % (threadName, time.ctime(time.time())))
      counter -= 1
      
if __name__ == '__main__':
    
    url='http://10.2.10.123:8080/shot.jpg' #Filips telefon
    #url='http://10.2.2.118:8080/shot.jpg' #Arons telefon
    
    t1 = imageFeed(url, "Thread-1")
    t2 = myThread(2, "Thread-2", 1)
    
    t1.start()
    t2.start()
    t1.join()   #Väntar på att tråden ska bli klar!
    t2.join()   #Väntar på att tråden ska bli klar!
    print("Threads done")

        