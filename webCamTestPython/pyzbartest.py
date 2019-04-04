# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 10:18:46 2019

@author: nilss
"""

from pyzbar import pyzbar
import argparse
import datetime
#import imutils
import time
import cv2

if __name__ == '__main__':
        print('Press "q" to quit')
        
        capture = cv2.VideoCapture(0)
        time.sleep(1)

        if capture.isOpened():  # try to get the first frame
                frame_captured, frame = capture.read()
        else:
                frame_captured = False

        while frame_captured:
            time.sleep(0.1) #Delay for easier console reading
            #frame = cv2.cvtColor(frame, cv2.COLOR_)
            # find the barcodes in the frame and decode each of the barcodes
            barcodes = pyzbar.decode(frame)
            marker_coords = [];
            # loop over the detected barcodes
            for barcode in barcodes:
                	# extract the bounding box location of the barcode and draw
            		# the bounding box surrounding the barcode on the image
            		(x, y, w, h) = barcode.rect
            		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
             
            		# the barcode data is a bytes object so if we want to draw it
            		# on our output image we need to convert it to a string first
            		barcodeData = barcode.data.decode("utf-8")
            		barcodeType = barcode.type
             
            		# draw the barcode data and barcode type on the image
            		text = "{} ({})".format(barcodeData, barcodeType)
            		cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            print("--------------------")
            #frame = cv2.resize(frame, (1210,720))
            #if(len(marker_coords)>=3):
                #print("yo")
                #cv2.line(frame,marker_coords[0],marker_coords[2],(255,0,0),5)
            frame = cv2.resize(frame, (1210,720))
            cv2.imshow('Detection Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            frame_captured, frame = capture.read()
                
        
        
        # When everything done, release the capture
        capture.release()
        cv2.destroyAllWindows()