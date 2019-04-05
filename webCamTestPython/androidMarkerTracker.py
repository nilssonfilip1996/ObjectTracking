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
import time
import numpy as np

def draw_quadrant(ox,oy,frame):
    height, width, bla = frame.shape
    start_row, start_col = int(0), int(0)
    end_row, end_col = int(height), int(width)
    # vertical line
    cv2.line(frame, (ox,start_row), (ox,end_row), (255,0,0),10)
    # horizontal line
    cv2.line(frame, (start_col, oy), (end_col, oy), (255,0,0),10)

if __name__ == '__main__':
        print('Press "q" to quit')
        
        url='http://10.2.10.123:8080/shot.jpg' #Filips telefon
        #url='http://10.2.2.118:8080/shot.jpg' #Arons telefon
        

        while True:
            #time.sleep(0.1) #Delay for easier console reading
            # Use urllib to get the image from the IP camera
            imgResp = urllib.request.urlopen(url)
    
            # Numpy to convert into a array
            imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
            
            # Finally decode the array to OpenCV usable format
            frame = cv2.imdecode(imgNp,-1)
            #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            markers = detect_markers(frame)
            unique_markers = []
            marker_ids = []
            for marker in markers:
                if(marker.id not in marker_ids):    #This removes duplicate markers. Dunno why every marker is registered twice
                    unique_markers.append(marker)
                    marker_ids.append(marker.id)
                    marker.highlite_marker(frame)
                    #print("value: " + str(marker.id), "coordinate: " + str(marker.center))
            #print("--------------------")
            if(len(unique_markers)==4):
                unique_markers.sort(key=lambda x: x.id) #Sort the quadrants
                x_tot = 0
                y_tot = 0
                for i in range(4): #Draw a rectangle
                    x_tot+=unique_markers[i].center[0]
                    y_tot+=unique_markers[i].center[1]
                    if(i!=3):
                        cv2.line(frame,unique_markers[i].center,unique_markers[i+1].center,(255,0,0),10)
                    else:
                        cv2.line(frame,unique_markers[i].center,unique_markers[0].center,(255,0,0),10)
                xOrigo = int(x_tot/4)
                yOrigo = int(y_tot/4)
                cv2.line(frame,(xOrigo-10,yOrigo-10,),(xOrigo+10,yOrigo+10,),(0,0,255),10)  #Mark origo
                cv2.line(frame,(xOrigo-10,yOrigo+10,),(xOrigo+10,yOrigo-10,),(0,0,255),10)
                
                #Skicka till Aron här
                draw_quadrant(xOrigo, yOrigo, frame)
            frame = cv2.resize(frame, (1210,720))
            cv2.imshow('Detection Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                

        cv2.destroyAllWindows()
        