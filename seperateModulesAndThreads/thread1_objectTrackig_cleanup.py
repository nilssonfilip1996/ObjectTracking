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
import math
from collections import Counter
import dictdiffer


class imageFeed(threading.Thread):
    def __init__(self, url, name):
        threading.Thread.__init__(self)
        self.url = url                      #Url for camera feed
        self.name = name                    #Thread name
        self.d_list = []                    #Collection of x recent readings
        self.prev_reading = {}              #To keep track of the last succesful reading
        
    def run(self):
      print ("Starting " + self.name)
      self.stream()
      print ("Exiting " + self.name)
        
    def stream(self):
        print('Press "q" to quit')
        counter=0
        while True:
            unique_markers = {}
            marker_ids = []
                
            frame = self.getMobileFrame(self.url)
            #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if(counter==5):
                if(self.evaluateMarkerSequence()):
                    print("Major diff detected!")
                    print()
                counter=0
            markers = detect_markers(frame)
            for marker in markers:
                if(marker.id not in marker_ids):    #This removes duplicate markers. Dunno why every marker is registered twice
                    unique_markers[marker.id] = marker.center
                    marker_ids.append(marker.id)
                    marker.highlite_marker(frame)
            self.d_list.append(unique_markers)
            frame = cv2.resize(frame, (1210,720))
            cv2.imshow('Detection Frame', frame)
            counter+=1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
        cv2.destroyAllWindows()
       
    def evaluateMarkerSequence(self):
        full_d = {}
        current_reading = {}
        for d in self.d_list:   #d_list is a list of the 5 most recent readings.
            for d_key in d: 
                if(not  d_key in full_d):
                    full_d[d_key] = []          #full_d is a single dict holding all info from the 5 most recent readings.
                full_d[d_key].append(d[d_key])
        for d_key in full_d:
            c = Counter(full_d[d_key])          
            value = c.most_common()[0][0]       #Get the most frequent value from the 5 most recent readings
            current_reading[d_key] = value      #current_reading holds the most frequent values from the 5 most recent readings.
        major_diff_detected = False
        for diff in list(dictdiffer.diff(self.prev_reading, current_reading)):
            if(major_diff_detected):
                break
            if(diff[0]=='change'):
                m1 = diff[2][0]         #Old reading
                m2 = diff[2][1]         #New reading
                if(not isInBoundary(m1, m2, 4)): #diff in 4 pixels mean actual movement.
                    major_diff_detected = True
            else:
                major_diff_detected = True
        self.prev_reading = current_reading
        self.d_list = []
        if(major_diff_detected):
            return True
        else:
            return False
    
    def getMobileFrame(self, url):
        # Use urllib to get the image from the IP camera
        imgResp = urllib.request.urlopen(url)
        # Numpy to convert into a array
        imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
        # Finally decode the array to OpenCV usable format
        return cv2.imdecode(imgNp,-1)
        
                
def isInBoundary(coord1, coord2, r): 
  
    x1 = math.pow((coord2[0]-coord1[0]), 2) 
    y1 = math.pow((coord2[1]-coord1[1]), 2) 
    hyp = math.sqrt(x1 + y1) # distance between the centre and given point 
    return (hyp<r)
      
if __name__ == '__main__':
    url='http://10.2.10.123:8080/shot.jpg' #Filips telefon
    t1 = imageFeed(url, "Thread-1")
    t1.start()
    t1.join()   #Väntar på att tråden ska bli klar!
    print("Threads done")

        