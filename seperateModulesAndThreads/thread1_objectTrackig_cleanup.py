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
from collections import Counter
import dictdiffer
import datetime

from helper_module import isInBoundary
from thread2_EventHandling import worker

#width = 95.5
#height = 51
#cm_to_pixelsX = width/1920
#cm_to_pixelsY = height/1080


class imageFeed(threading.Thread):
    def __init__(self, url, name, worker, stopper):
        threading.Thread.__init__(self)
        self.url = url                      #Url for camera feed
        self.name = name                    #Thread name
        self.d_list = []                    #Collection of x recent readings
        self.prev_reading = {}              #To keep track of the last succesful reading
        
        self.worker = worker
        self.stopper = stopper
        
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
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if(counter==5):
                print(datetime.datetime.now().time())
                if(self.evaluateMarkerSequence()):
                    print("Major diff detected!")
                    print()
                counter=0
            markers = detect_markers(frame)
            for marker in markers:
                if(marker.id not in marker_ids):    #This removes duplicate markers. Dunno why every marker is registered twice
                    unique_markers[marker.id] = marker.center
                    #unique_markers[marker.id] =(round(marker.center[0]*cm_to_pixelsX,1),round(marker.center[1]*cm_to_pixelsY,1))
                    marker_ids.append(marker.id)
                    marker.highlite_marker(frame)
            self.d_list.append(unique_markers)
            frame = cv2.resize(frame, (1210,720))
            cv2.imshow('Detection Frame', frame)
            counter+=1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stopper.set()
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
            if(diff[0]=='change'):
                m1 = diff[2][0]         #Old reading
                m2 = diff[2][1]         #New reading
                if(not isInBoundary(m1, m2, 1)): #diff in 1 cm mean actual movement.
                    major_diff_detected = True
                    aDict = createChangeDict(diff)
                    self.worker.enQueue(aDict)
            else:   
                eventList = diff[2]
                for e in eventList:
                    aDict = createAddOrRemoveDict(diff[0],e)
                    self.worker.enQueue(aDict)
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
    markerId = contenttuple[1][0] #Only used for change event
    prevCoord = eventList[0]
    currCoord = eventList[1]
    aDict = {'event':'change', 
             'id' : markerId,
             'previousLocation': {'x':prevCoord[0],'y':prevCoord[1]},
             'currentLocation': {'x':currCoord[0],'y':currCoord[1]}}
    return aDict

def createAddOrRemoveDict(eventType, event):
    markerId = event[0]
    coord = event[1]
    aDict = {'event': eventType,
             'id':markerId,
             'currentLocation': {'x':coord[0],'y':coord[1]}}
    return aDict          
      
if __name__ == '__main__':
    url='http://10.2.5.219:8080/shot.jpg' #Filips telefon
    #url='http://192.168.1.59:8080/shot.jpg' #Filips telefon
    stopper = threading.Event()
    t2 = worker("worker",stopper)
    t2.daemon = True
    t2.start()
    t1 = imageFeed(url, "Thread-1", t2, stopper)
    t1.start()

    t1.join()   #Väntar på att tråden ska bli klar!
    t2.join()
    print("Threads done")

        