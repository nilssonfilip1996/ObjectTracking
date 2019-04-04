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
        
        capture = cv2.VideoCapture(0)

        if capture.isOpened():  # try to get the first frame
                frame_captured, frame = capture.read()
        else:
                frame_captured = False

        while frame_captured:
            time.sleep(0.1) #Delay for easier console reading
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            markers = detect_markers(frame)
            marker_coords = [];
            for marker in markers:
                    marker.highlite_marker(frame)
                    marker_coords.append(marker.center)
                    print("value: " + str(marker.id), "coordinate: " + str(marker.center))
            print("--------------------")
            #frame = cv2.resize(frame, (1210,720))
            if(len(marker_coords)>=3):
                #print("yo")
                cv2.line(frame,marker_coords[0],marker_coords[2],(255,0,0),5)
            frame = cv2.resize(frame, (1210,720))
            cv2.imshow('Detection Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            frame_captured, frame = capture.read()
                
        
        
        # When everything done, release the capture
        capture.release()
        cv2.destroyAllWindows()