#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    This is the main file of the program. 
    Connect the IP-camera before running this file.
    To quit the program shut down the Kinect window.
    
    Current limitations: Only one person can be visible
    for the system to capture that persons movements correctly.
    
    @author: Aron Polner & Filip Nilsson, 19/5/2019
    
    This code is an adaption of PyKinectV2
    originally created by Vlad Kolesnikov. 
    His github: https://github.com/Kinect/PyKinect2
"""

from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime

import ctypes
import _ctypes
import pygame
import sys
import threading
import time
import datetime

from PyMarkerTracking_Thread import imageFeed
from PyWorker_Thread import worker
import paho.mqtt.client as mqtt

# colors for drawing different bodies 
SKELETON_COLORS = [pygame.color.THECOLORS["red"], 
                  pygame.color.THECOLORS["blue"], 
                  pygame.color.THECOLORS["green"], 
                  pygame.color.THECOLORS["orange"], 
                  pygame.color.THECOLORS["purple"], 
                  pygame.color.THECOLORS["yellow"], 
                  pygame.color.THECOLORS["violet"]]


class BodyGameRuntime(object):
    def __init__(self, name, workerInstance, stopper):
        print()
        pygame.init()
        print()
        self.name = name
        self.worker = workerInstance
        self.stopper = stopper
        #-------------Use this method for publishing events!-------------
        #The format you pass as argument is the same format that is delivered to connected clients.
#        self.worker.enQueue({'work': 'sent',
#                             'from': 'kinect',
#                             'thread': ''})
        #----------------------------------------------------------------
        # Used to manage how fast the screen updates
        self._clock = pygame.time.Clock()

        # Set the width and height of the screen [width, height]
        self._infoObject = pygame.display.Info()
        self._screen = pygame.display.set_mode((self._infoObject.current_w >> 1, self._infoObject.current_h >> 1), 
                                               pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)

        pygame.display.set_caption("El01")

        # Loop until the user clicks the close button.
        self._done = False

        # Used to manage how fast the screen updates
        self._clock = pygame.time.Clock()

        # Kinect runtime object, we want only color and body frames 
        self._kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)

        # back buffer surface for getting Kinect color frames, 32bit color, width and height equal to the Kinect color frame size
        self._frame_surface = pygame.Surface((self._kinect.color_frame_desc.Width, self._kinect.color_frame_desc.Height), 0, 32)

        # here we will store skeleton data 
        self._bodies = None
        
        # roatiotion variables
        
        self._current_rotation = None
        self._previous_rotation = None
        
    def draw_body_bone(self, joints, jointPoints, color, joint0, joint1):
        joint0State = joints[joint0].TrackingState;
        joint1State = joints[joint1].TrackingState;

        # both joints are not tracked
        if (joint0State == PyKinectV2.TrackingState_NotTracked) or (joint1State == PyKinectV2.TrackingState_NotTracked): 
            return

        # both joints are not *really* tracked
        if (joint0State == PyKinectV2.TrackingState_Inferred) and (joint1State == PyKinectV2.TrackingState_Inferred):
            return

        # ok, at least one is good 
        start = (jointPoints[joint0].x, jointPoints[joint0].y)
        end = (jointPoints[joint1].x, jointPoints[joint1].y)

        try:
            pygame.draw.line(self._frame_surface, color, start, end, 8)
        except: # need to catch it due to possible invalid positions (with inf)
            pass

    def draw_body(self, joints, jointPoints, color):
        # Torso
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_Head, PyKinectV2.JointType_Neck);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_Neck, PyKinectV2.JointType_SpineShoulder);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_SpineMid);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineMid, PyKinectV2.JointType_SpineBase);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_ShoulderRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_ShoulderLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipLeft);
    
        # Right Arm    
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ShoulderRight, PyKinectV2.JointType_ElbowRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ElbowRight, PyKinectV2.JointType_WristRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristRight, PyKinectV2.JointType_HandRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HandRight, PyKinectV2.JointType_HandTipRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristRight, PyKinectV2.JointType_ThumbRight);

        # Left Arm
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ShoulderLeft, PyKinectV2.JointType_ElbowLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_ElbowLeft, PyKinectV2.JointType_WristLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_HandLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HandLeft, PyKinectV2.JointType_HandTipLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_ThumbLeft);

        # Right Leg
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HipRight, PyKinectV2.JointType_KneeRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_KneeRight, PyKinectV2.JointType_AnkleRight);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_AnkleRight, PyKinectV2.JointType_FootRight);

        # Left Leg
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_HipLeft, PyKinectV2.JointType_KneeLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_KneeLeft, PyKinectV2.JointType_AnkleLeft);
        self.draw_body_bone(joints, jointPoints, color, PyKinectV2.JointType_AnkleLeft, PyKinectV2.JointType_FootLeft);

    def draw_color_frame(self, frame, target_surface):
        target_surface.lock()
        address = self._kinect.surface_as_array(target_surface.get_buffer())
        ctypes.memmove(address, frame.ctypes.data, frame.size)
        del address
        target_surface.unlock()

    def run(self):
        print("Starting " + self.name)
        previousTime = datetime.datetime.now()
        # -------- Main Program Loop -----------
        while not self._done:
            # --- Main event loop
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    self._done = True # Flag that we are done so we exit this loop
                 
                elif event.type == pygame.VIDEORESIZE: # window resized
                    self._screen = pygame.display.set_mode(event.dict['size'], 
                                               pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)

            # --- Getting frames and drawing  
            # --- Woohoo! We've got a color frame! Let's fill out back buffer surface with frame's data 
            if self._kinect.has_new_color_frame():
                frame = self._kinect.get_last_color_frame()
                self.draw_color_frame(frame, self._frame_surface)
                frame = None

            # --- Cool! We have a body frame, so can get skeletons
            if self._kinect.has_new_body_frame(): 
                self._bodies = self._kinect.get_last_body_frame()

            # --- draw skeletons to _frame_surface
            if self._bodies is not None: 
                for i in range(0, self._kinect.max_body_count):
                    body = self._bodies.bodies[i]
                    if not body.is_tracked:
                        continue 
                    
                    '''El01 CODE STARTS HERE'''
                    
                    # ROTATION
                    
                    '''
                    The code below retreives the Z value of each shoulder joint.
                    A difference (diff_shoulders) is then calculated. Depending 
                    on this difference either of the three events are triggered:
                        
                                        "facing table"
                                        "facing left"
                                        "facing right"
                    
                    The depth that currently triggers an event is 0.1m (10cm).
                    A filter is applied to the algorithm to only allow new events
                    to be triggered if they are 500ms (0.5s) apart. Once a new 
                    event occurs it is formated to JSON and enQueued to the worker
                    thread.
                    '''
                    
                    right_shoulder_z = body.joints[PyKinectV2.JointType_ShoulderRight].Position.z;
                    left_shoulder_z = body.joints[PyKinectV2.JointType_ShoulderLeft].Position.z;
                    diff_shoulders = left_shoulder_z - right_shoulder_z
                    
                    if (abs(diff_shoulders) < 0.10):
                        self._current_rotation = "facing table"
                    elif(diff_shoulders > 0):
                        self._current_rotation = "facing left"
                    else:
                        self._current_rotation = "facing right"
                    
                    currentTime = datetime.datetime.now()
                    if (self._current_rotation != self._previous_rotation):
                        diff = currentTime-previousTime
                        diff_in_millis = diff.total_seconds()*1000

                        if(diff_in_millis>500):
                            event_triggered = True
                            previousTime = currentTime
                        
                    if(event_triggered):
                        print(self._current_rotation)
                        self.worker.enQueue({"type" : "player",
                                             "event": "rotation",
                                             "localTime" : str(currentTime)[:-4],
                                             "previousRotation" : self._previous_rotation,
                                             "currentRotation" : self._current_rotation})
                        #print(self._current_rotation)
                        self._previous_rotation = self._current_rotation
                        event_triggered = False
                                
                    ''' El01 CODE ENDS HERE '''
                    
                    joints = body.joints
                    # convert joint coordinates to color space 
                    joint_points = self._kinect.body_joints_to_color_space(joints)
                    
                    self.draw_body(joints, joint_points, SKELETON_COLORS[i])

            # --- copy back buffer surface pixels to the screen, resize it if needed and keep aspect ratio
            # --- (screen size may be different from Kinect's color frame size) 
            
            # this can be removed - updates the frames to the thing
            h_to_w = float(self._frame_surface.get_height()) / self._frame_surface.get_width()
            target_height = int(h_to_w * self._screen.get_width())
            surface_to_draw = pygame.transform.scale(self._frame_surface, (self._screen.get_width(), target_height));
            self._screen.blit(surface_to_draw, (0,0))
            surface_to_draw = None
            pygame.display.update()

            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            # --- Limit to 60 frames per second
            self._clock.tick(60)

        # Close our Kinect sensor, close the window and quit.
        self._kinect.close()
        pygame.quit()
        self.stopper.set()      #Important for stopping marker- and worker thread on closing kinect window!
        print("Exiting " + self.name)


__main__ = "Kinect v2 El01"

# MQTT broker credentials are entered below
client_id = "DummyClient"
client = mqtt.Client(client_id)
client.username_pw_set("twzdgqki", "aB6nkIbUQ7Nx")
client.connect('m24.cloudmqtt.com', 13583, 60)

# The URL of the IP-camera is inserted below
url='http://10.2.5.219:8080/shot.jpg' 

# Thread logic for the worker as well as the Kinect are below
stopper = threading.Event()
wThread = worker("Worker-thread",stopper, client)
wThread.start()
mThread = imageFeed(url, "Marker-thread", wThread, stopper)
mThread.start()
game = BodyGameRuntime("Kinect-thread",wThread,stopper);
game.run();
mThread.join()
wThread.join()
print("Threads done")