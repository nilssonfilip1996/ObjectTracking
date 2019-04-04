#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 09:48:25 2019

@author: orgel
"""

import cv2, time

# create an object. 0 for external camera
video = cv2.VideoCapture(0)

while(True):

    # create a fram object
    check, frame = video.read()
    
    # convert to grayscale
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # capture the height and width
    height, width = frame.shape[:2]

    # frame shape is 720, 1280 - crop that
    start_row, start_col = int(0), int(0)
    end_row, end_col = int(height * .5), int(width)
    cropped_top = gray[start_row:end_row, start_col:end_col]
        #print(start_row, end_row)
        #print(start_col, end_col)

    # show the frame
    cv2.imshow("capturing", cropped_top)
    
    # for playing
    key=cv2.waitKey(1)
    
    if key == ord('q'):
        break

# shut down camera
video.release()
cv2.destroyAllWindows

