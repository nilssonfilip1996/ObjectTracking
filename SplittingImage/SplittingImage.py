#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 09:48:25 2019

@author: orgel
"""

import cv2, time

# create an object. 0 for external camera
video = cv2.VideoCapture(0)

def find_quadrant(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONUP:

        print("you pressed lbuttonup")

while(True):

    # create a fram object
    check, frame = video.read()
    
    # convert to grayscale
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # capture the height and width
    height, width = frame.shape[:2]
    #print(height)

    # vertical line in the middle
    start_row, start_col = int(0), int(0)
    middle_row, end_col = int(height * .5), int(width)
    cv2.line(gray, (start_col, middle_row),(end_col, middle_row), 10)

    # horizontal line in the middle
    middle_col, start_row, end_row = int(width * .5), int(0), int(height)
    cv2.line(gray, (middle_col, start_row), (middle_col, end_row), 10)

    # cropped_top = gray[start_row:end_row, start_col:end_col]
        #print(start_row, end_row)
        #print(start_col, end_col)

    # show the frame
    cv2.imshow("capturing", gray)

    cv2.setMouseCallback("capturing", find_quadrant)
    
    # for playing
    key=cv2.waitKey(1)
    
    if key == ord('q'):
        break

# shut down camera
video.release()
cv2.destroyAllWindows

