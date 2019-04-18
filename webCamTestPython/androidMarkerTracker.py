# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 12:12:48 2019

@author: nilss
"""

from __future__ import print_function
import urllib
import cv2
from ar_markers import detect_markers
from ar_markers.marker import HammingMarker
import numpy as np
import math

def draw_quadrant(ox,oy,frame):
    height, width, bla = frame.shape
    start_row, start_col = int(0), int(0)
    end_row, end_col = int(height), int(width)
    # vertical line
    cv2.line(frame, (ox,start_row), (ox,end_row), (255,0,0),10)
    # horizontal line
    cv2.line(frame, (start_col, oy), (end_col, oy), (255,0,0),10)
    
def getMobileFrame(url):
    # Use urllib to get the image from the IP camera
    imgResp = urllib.request.urlopen(url)

    # Numpy to convert into a array
    imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
    
    # Finally decode the array to OpenCV usable format
    return cv2.imdecode(imgNp,-1)

def evaluateFP_marker(prevCoord, currentCoord, currentQ, origo):
    if(currentCoord[0]>origo[0] and currentCoord[1]<origo[1]):
        return 1
    if(currentCoord[0]>origo[0] and currentCoord[1]>origo[1]):
        return 2
    if(currentCoord[0]<origo[0] and currentCoord[1]>origo[1]):
        return 3
    if(currentCoord[0]<origo[0] and currentCoord[1]<origo[1]):
        return 4
    return currentQ

def isInBoundary(coord1, coord2, r): 
      
    x1 = math.pow((coord2[0]-coord1[0]), 2) 
    y1 = math.pow((coord2[1]-coord1[1]), 2) 
    hyp = math.sqrt(x1 + y1) # distance between the centre and given point 
    #print(hyp)
    return (hyp<r)
    
    


if __name__ == '__main__':
    print('Press "q" to quit')
    
    url='http://192.168.1.59:8080/shot.jpg' #Filips telefon
    #url='http://10.2.2.118:8080/shot.jpg' #Arons telefon
    fp_location = (0,0)
    fp_quadrant = 1

    while True:
        #time.sleep(0.1) #Delay for easier console reading
        frame = getMobileFrame(url)
        markers = detect_markers(frame)
        unique_markers = []
        corner_markers = []
        marker_ids = []
        fp_marker = None
        for marker in markers:
            if(marker.id not in marker_ids):    #This removes duplicate markers. Dunno why every marker is registered twice
                if(marker.id>0 and marker.id<5):    #corners have values 1,2,3,4
                    corner_markers.append(marker)
                if(marker.id==5):                   #First player marker
                    fp_marker = marker
                unique_markers.append(marker)
                marker_ids.append(marker.id)
                marker.highlite_marker(frame)
                #print("value: " + str(marker.id), "coordinate: " + str(marker.center))
        #print("--------------------")
        if(len(corner_markers)==4):
            corner_markers.sort(key=lambda x: x.id) #Sort the quadrants
            x_tot = 0
            y_tot = 0
            for i in range(4): #Draw a rectangle
                x_tot+=corner_markers[i].center[0]
                y_tot+=corner_markers[i].center[1]
                if(i!=3):
                    cv2.line(frame,corner_markers[i].center,corner_markers[i+1].center,(255,0,0),10)
                else:
                    cv2.line(frame,corner_markers[i].center,corner_markers[0].center,(255,0,0),10)
            xOrigo = int(x_tot/4)
            yOrigo = int(y_tot/4)
            cv2.line(frame,(xOrigo-10,yOrigo-10,),(xOrigo+10,yOrigo+10,),(0,0,255),10)  #Mark origo
            cv2.line(frame,(xOrigo-10,yOrigo+10,),(xOrigo+10,yOrigo-10,),(0,0,255),10)
            
            draw_quadrant(xOrigo, yOrigo, frame)
            if(fp_marker!=None):
                temp_quadrant = evaluateFP_marker(fp_location, fp_marker.center, fp_quadrant, (xOrigo, yOrigo,))
                if(temp_quadrant!= fp_quadrant):
                    fp_quadrant = temp_quadrant
                    print("Changed to quadrant: " + str(fp_quadrant))
                fp_location = fp_marker.center
        frame = cv2.resize(frame, (1210,720))
        cv2.imshow('Detection Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            

    cv2.destroyAllWindows()
        