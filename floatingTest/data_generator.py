# -*- coding: utf-8 -*-
"""
Created on Thu May 16 14:57:59 2019

@author: nilss
"""

from __future__ import print_function
import cv2
from ar_markers import detect_markers
import numpy as np
import urllib
import time

if __name__ == '__main__':
        print('Press "q" to quit')
        url='http://10.2.5.219:8080/shot.jpg' #Filips telefon
        
        counter = 0
        
        while(1):
            # Use urllib to get the image from the IP camera
            imgResp = urllib.request.urlopen(url)
            
            # Numpy to convert into a array
            imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
            
            # Finally decode the array to OpenCV usable format ;) 
            frame = cv2.imdecode(imgNp,-1)
            markers = detect_markers(frame)
            marker_ids = []
            for marker in markers:
                if(marker.id not in marker_ids):    #This removes duplicate markers. Dunno why every marker is registered twice
                    marker_ids.append(marker.id)
                    marker.highlite_marker(frame)
                    print("value: " + str(marker.id), "coordinate: " + str(marker.center))
                    file = open("test.txt", 'a')
                    file.write(str(marker.center) + "\n")
                    counter+=1
                    print(counter)
            if(counter>=1000):
                break
            print("--------------------")
            #frame = cv2.resize(frame, (1210,720))
            frame = cv2.resize(frame, (1210,720))
            cv2.imshow('Detection Frame', frame)
            
            # Quit if q is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
        file.close()
        cv2.destroyAllWindows()