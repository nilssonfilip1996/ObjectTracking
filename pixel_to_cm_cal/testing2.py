# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 14:51:07 2019

@author: Filip
"""

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


"""
Measgure width and height of camera of scene set variables width and height accordingly.
"""
width = 95.5
height = 51
cm_to_pixelsX = width/1920
cm_to_pixelsY = height/1080

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
        print(cm_to_pixelsX)
        while True:
            frame = getMobileFrame("http://10.2.5.219:8080/shot.jpg")
            #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            markers = detect_markers(frame)
            for marker in markers:
                    marker.highlite_marker(frame)
            if(len(markers)>0):
                m1 = markers[0].center
                print("m1 pixels:" + str(m1))
                print("m1 cm:" + str((m1[0]*cm_to_pixelsX, m1[1]*cm_to_pixelsY,)))
                print("------")
            frame = cv2.resize(frame, (1210,720))
            cv2.imshow('Test Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        cv2.destroyAllWindows()