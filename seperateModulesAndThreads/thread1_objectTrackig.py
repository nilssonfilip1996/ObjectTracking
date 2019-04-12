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
import math
from collections import Counter
import dictdiffer


class imageFeed(threading.Thread):
    def __init__(self, url, name):
        threading.Thread.__init__(self)
        self.url = url
        self.name = name
        #self.cap = cv2.VideoCapture('http://localhost:4747/mjpegfeed')
        #self.start()
        
    def run(self):
      print ("Starting " + self.name)
      self.stream()
      print ("Exiting " + self.name)
        
    def stream(self):
        print('Press "q" to quit')
        counter=0
        d_list = []
        prev_reading = {}
        current_reading = {}
        while True:
            #unique_markers = []
            unique_markers = {}
            marker_ids = []
                
            frame = self.getMobileFrame(self.url)
            #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if(counter==5):
                full_d = {}
                for d in d_list: #d_list is a list of the 5 most recent readings
                    for d_key in d: 
                        if(not  d_key in full_d):
                            full_d[d_key] = []          #full_d is a single dict holding all info from the 5 most recent readings.
                        full_d[d_key].append(d[d_key])
                for d_key in full_d:
                    c = Counter(full_d[d_key])          
                    value = c.most_common()[0][0]       #Get the most frequent value from the 5 most recent readings
                    current_reading[d_key] = value      #current_reading holds the most frequent values from the 5 most recent readings.
                diff_list = []
                major_diff_detected = False
                for diff in list(dictdiffer.diff(prev_reading, current_reading)):
                    if(diff[0]=='change'):
                        if(not isInBoundary(diff[2][0], diff[2][1], 4)): #diff in 4 pixels mean actual movement
                            diff_list.append((diff[1], diff[2]))
                            major_diff_detected = True
                    if(diff[0]=='add'):
                        print("Added " + str(diff[2]))
                    if(diff[0]=='remove'):
                        print("Removed " + str(diff[2]))
                if(major_diff_detected):
                    print("Change detected on: " + str(diff_list))
                prev_reading = current_reading
                current_reading = {}
                counter=0
                d_list = []
            markers = detect_markers(frame)
            for marker in markers:
                if(marker.id not in marker_ids):    #This removes duplicate markers. Dunno why every marker is registered twice
                    #unique_markers.append(marker)
                    unique_markers[marker.id] = marker.center
                    marker_ids.append(marker.id)
                    marker.highlite_marker(frame)
            print()
            d_list.append(unique_markers)
            frame = cv2.resize(frame, (1210,720))
            cv2.imshow('Detection Frame', frame)
            counter+=1
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
        
#        ret, frame = self.cap.read()
#        return frame
        
def checkDictEquality(od, nd):
    for k in nd.keys():
        if(k in od.keys()):
            if(not isInBoundary(od[k], nd[k], 4)):
                return False
        else:
            return False
    return True
                
def isInBoundary(coord1, coord2, r): 
  
    x1 = math.pow((coord2[0]-coord1[0]), 2) 
    y1 = math.pow((coord2[1]-coord1[1]), 2) 
    hyp = math.sqrt(x1 + y1) # distance between the centre and given point 
    #print(hyp)
    return (hyp<r)
                
    
    

#class myThread (threading.Thread):
#   def __init__(self, threadID, name, counter):
#      threading.Thread.__init__(self)
#      self.threadID = threadID
#      self.name = name
#      self.counter = counter
#      
#   def run(self):
#      print ("Starting " + self.name)
#      print_time(self.name, self.counter, 10)
#      print ("Exiting " + self.name)
#
#def print_time(threadName, delay, counter):
#   while counter:
#      time.sleep(delay)
#      print ("%s: %s" % (threadName, time.ctime(time.time())))
#      counter -= 1
      
if __name__ == '__main__':
    
    url='http://10.2.10.123:8080/shot.jpg' #Filips telefon
    #url='http://10.2.2.118:8080/shot.jpg' #Arons telefon
    
    t1 = imageFeed(url, "Thread-1")
    #t2 = myThread(2, "Thread-2", 1)
    
    t1.start()
    #t2.start()
    t1.join()   #Väntar på att tråden ska bli klar!
    #t2.join()   #Väntar på att tråden ska bli klar!
    print("Threads done")

        