# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 12:28:52 2019

@author: Filip
"""
import urllib
import cv2
import numpy as np
from ar_markers import detect_markers
import math

cm_to_pixels = 93.3/1080

def getMobileFrame(url):
        # Use urllib to get the image from the IP camera
        imgResp = urllib.request.urlopen(url)
        # Numpy to convert into a array
        imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
        # Finally decode the array to OpenCV usable format
        return cv2.imdecode(imgNp,-1)

def getDistance(coord1, coord2): 
      
    x1 = math.pow((coord2[0]-coord1[0]), 2) 
    y1 = math.pow((coord2[1]-coord1[1]), 2) 
    hyp = math.sqrt(x1 + y1) # distance between the centre and given point 
    #print(hyp)
    return hyp

if __name__ == '__main__':
        print('Press "q" to quit')
        print(cm_to_pixels)
        counter=0
        sums=0
        while True:
            frame = getMobileFrame("http://192.168.1.59:8080/shot.jpg")
            #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            markers = detect_markers(frame)
            for marker in markers:
                    marker.highlite_marker(frame)
            if(len(markers)==4):
                m1 = markers[0].center
                m2 = markers[2].center
                cv2.line(frame,m1,m2,(255,0,0),10)
                sums+=getDistance(m1,m2)
                counter+=1
                if(counter==20):
                    dist = sums/20
                    print(round(dist,2))
                    counter=0
                    sums=0
            frame = cv2.resize(frame, (1210,720))
            cv2.imshow('Test Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        cv2.destroyAllWindows()