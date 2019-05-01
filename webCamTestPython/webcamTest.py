# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 10:29:02 2019

@author: nilss

Follow this guide in order to use dependancies: https://pypi.org/project/ar-markers/
"""

from __future__ import print_function
import cv2
from ar_markers import detect_markers
import time
if __name__ == '__main__':
        print('Press "q" to quit')
        
        frame = cv2.imread('test.jpg',1)
        time.sleep(0.1) #Delay for easier console reading
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        markers = detect_markers(frame)
        marker_coords = [];
        for marker in markers:
                marker.highlite_marker(frame)
                marker_coords.append(marker.center)
                print("value: " + str(marker.id), "coordinate: " + str(marker.center))
        print("--------------------")
        #frame = cv2.resize(frame, (1210,720))
        frame = cv2.resize(frame, (1210,720))
        cv2.imshow('Detection Frame', frame)
                
        #cv2.destroyAllWindows()