# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 16:54:44 2019

@author: nilss
"""

# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
from ar_markers import detect_markers
import time
import cv2
 
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (1920, 1080)
camera.framerate = 32
rawCapture = PiRGBArray(camera)
 
# allow the camera to warmup
time.sleep(0.1)
 
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    #time.sleep(0.5)
    image = frame.array
    
    markers = detect_markers(image)
    marker_coords = []
    for marker in markers:
        marker.highlite_marker(image)
        marker_coords.append(marker.center)
        print("value: " + str(marker.id), "coordinate: " + str(marker.center))
    print("--------------------")
    if(len(marker_coords)==4):
            cv2.line(image,marker_coords[0],marker_coords[3],(255,0,0),5)
    image = cv2.resize(image, (1210,720))
        #cv2.imshow('Detection Frame', frame)

    # show the frame
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
            break

