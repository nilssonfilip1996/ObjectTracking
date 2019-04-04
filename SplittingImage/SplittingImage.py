#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 09:48:25 2019

@author: orgel
"""

import cv2, time
from ar_markers import detect_markers
from ar_markers.marker import HammingMarker
import numpy as np

# create an object. 0 for external camera
video = cv2.VideoCapture(0)

# change the serolution of the video stream
video.set(3, 640)
video.set(4, 460)

def find_quadrant(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONUP:
        print("x: {}, y: {}".format(x, y))
        # quadrant 1
        if x > 230 and y < 320:
            print("first quadrant")
            

while(True):

    # create a fram object
    check, frame = video.read()
    
    # convert to grayscale
    #gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = frame

    # capture the height and width
    height, width = frame.shape[:2]



    # vertical line in the middle
    start_row, start_col = int(0), int(0)
    middle_row, end_col = int(height * .5), int(width)
    cv2.line(gray, (start_col, middle_row),(end_col, middle_row), 10)

    # horizontal line in the middle
    middle_col, start_row, end_row = int(width * .5), int(0), int(height)
    cv2.line(gray, (middle_col, start_row), (middle_col, end_row), 10)
    
    markers = detect_markers(gray)
    #print("length of marker data structure: ", len(markers))
    if markers:
        markers[0].highlite_marker(gray)
        print("id: {}, center: {}".format(markers[0].id, markers[0].center))

    # show the frame
    cv2.imshow("capturing", gray)

    cv2.setMouseCallback("capturing", find_quadrant, gray)
    
    # for playing
    key=cv2.waitKey(1)
    
    if key == ord('q'):
        break

# shut down camera
video.release()
cv2.destroyAllWindows



# --------------------- 

 #   font = cv2.FONT_HERSHEY_SIMPLEX
 #   cv2.putText(gray, "Quadrant code", (200,200), font, 1, (255,255,255), 2, cv2.LINE_AA)

