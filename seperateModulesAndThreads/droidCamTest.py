# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 14:45:46 2019

@author: nilss
"""

import numpy as np
import cv2

cap = cv2.VideoCapture('http://localhost:4747/mjpegfeed')

while(True):
    ret, frame = cap.read()

    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()