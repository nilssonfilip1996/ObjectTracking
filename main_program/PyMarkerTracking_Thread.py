#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Marker tracking class.

The heart or the marker tracking. All logic is run on a thread that is
processing frames from an IP-based camera. Image processing is done
on each frame to detect and track 2D markers. A filter is applied
by collecting 5 consecutive frames in a dictionary. An average of the
five frames is calculated. The latest calculate image are compared to
the previously collected images. If differences are detected then it 
means events has occurred. 

@author: Aron Polner & Filip Nilsson 9/5/2019
"""

import urllib
import cv2
from ar_markers import detect_markers
import threading
import numpy as np
from collections import Counter
import dictdiffer
import datetime
import math


class imageFeed(threading.Thread):
    def __init__(self, url, name, worker, stopper):
        threading.Thread.__init__(self)
        self.url = url                            # Url for camera feed
        self.name = name                          # Thread name
        self.d_list = []                          # Collection of x recent readings
        self.prev_reading = {}                    # To keep track of the last succesful reading  
        self.worker = worker
        self.stopper = stopper
        
    def run(self):
      print ("Starting " + self.name)
      self.stream()
      print ("Exiting " + self.name)
        
    def stream(self):
        print('Press "q" to quit')
        counter=0
        while not self.stopper.is_set():
            unique_markers = {}
            marker_ids = []
            frame = self.getMobileFrame(self.url)
            if(counter==5):
                self.evaluateMarkerSequence()
                counter=0
            markers = detect_markers(frame)
            for marker in markers:
                if(marker.id not in marker_ids):  # This removes duplicate markers.
                    unique_markers[marker.id] = marker.center
                    marker_ids.append(marker.id)
                    marker.highlite_marker(frame)
            self.d_list.append(unique_markers)
            frame = cv2.resize(frame, (1210,720))
            cv2.imshow('Detection Frame', frame)
            counter+=1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Close the kinect windows to terminate the program")    
        cv2.destroyAllWindows()
       
    def evaluateMarkerSequence(self):
        full_d = {}
        current_reading = {}
        for d in self.d_list:                    # d_list is a list of the 5 most recent readings.
            for d_key in d: 
                if(not  d_key in full_d):
                    full_d[d_key] = []           # full_d is a single dict holding all info from the 5 most recent readings.
                full_d[d_key].append(d[d_key])
        for d_key in full_d:
            c = Counter(full_d[d_key])          
            value = c.most_common()[0][0]        # Get the most frequent value from the 5 most recent readings
            current_reading[d_key] = value       # current_reading holds the most frequent values from the 5 most recent readings.
        major_diff_detected = False
        for diff in list(dictdiffer.diff(self.prev_reading, current_reading)):
            if(diff[0]=='change'):
                m1 = diff[2][0]                  # Old reading
                m2 = diff[2][1]                  # New reading
                if(not isInBoundary(m1, m2, 2)): # diff in 2 pixels mean actual movement.
                    major_diff_detected = True
                    aDict = createChangeDict(diff)
                    self.worker.enQueue(aDict)   # Pass event to worker
            else:   
                eventList = diff[2]
                for e in eventList:
                    aDict = createAddOrRemoveDict(diff[0],e)
                    self.worker.enQueue(aDict)   # Pass event to worker
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
        
def createChangeDict(contenttuple):
    eventList = contenttuple[2]
    markerId = contenttuple[1][0]               # Only used for change event
    prevCoord = eventList[0]
    currCoord = eventList[1]
    print("Moved marker " + str(markerId))
    aDict = {'event':'change',
             'localTime': str(datetime.datetime.now().time())[:-4],
             'id' : markerId,
             'previousLocation': {'x':prevCoord[0],'y':prevCoord[1]},
             'currentLocation': {'x':currCoord[0],'y':currCoord[1]}}
    return aDict

def createAddOrRemoveDict(eventType, event):
    markerId = event[0]
    coord = event[1]
    if(eventType=='add'):
        print("Added marker " + str(markerId))
        aDict = {'event': eventType,
                 'localTime': str(datetime.datetime.now().time())[:-4],
                 'id':markerId,
                 'previousLocation': {'x':'N/A','y':'N/A'},
                 'currentLocation': {'x':coord[0],'y':coord[1]}}
    else:
        print("Removed marker " + str(markerId))
        aDict = {'event': eventType,
                 'localTime': str(datetime.datetime.now().time())[:-4],
                 'id':markerId,
                 'previousLocation': {'x':coord[0],'y':coord[1]},
                 'currentLocation': {'x':'N/A','y':'N/A'}}
    return aDict 

def isInBoundary(coord1, coord2, r): 
  
    x1 = math.pow((coord2[0]-coord1[0]), 2) 
    y1 = math.pow((coord2[1]-coord1[1]), 2) 
    hyp = math.sqrt(x1 + y1)                    # Distance between the centre and given point 
    return (hyp<r)          