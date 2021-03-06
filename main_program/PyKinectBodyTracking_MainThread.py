"""
This is the main file of the program.
Run this file.

@author: orgel & Filip
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
        pygame.init()
        self.name = name
        self.worker = workerInstance
        self.stopper = stopper
        #-------------Use this method for publishing events!-------------
        #The format you pass as argument is the same format that is delivered to connected clients.
        self.worker.enQueue({'work': 'sent',
                             'from': 'kinect',
                             'thread': ''})
        #----------------------------------------------------------------
        # Used to manage how fast the screen updates
        self._clock = pygame.time.Clock()

        # Set the width and height of the screen [width, height]
        self._infoObject = pygame.display.Info()
        self._screen = pygame.display.set_mode((self._infoObject.current_w >> 1, self._infoObject.current_h >> 1), 
                                               pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)

        pygame.display.set_caption("Kinect for Windows v2 Body Game")

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
        
        # here we will store state data
        self._current_rotation = None
        self._left_hand_state = None
        self._right_hand_state = None
        
        self._previous_rotation = None
        self._previous_left_hand_state = None
        self._previous_right_hand_state = None
    

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
        # -------- Main Program Loop -----------
        while not self._done:
            # --- Main event loop
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    self._done = True # Flag that we are done so we exit this loop

                elif event.type == pygame.VIDEORESIZE: # window resized
                    self._screen = pygame.display.set_mode(event.dict['size'], 
                                               pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE, 32)
                    
            # --- Game logic should go here

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
                    
                    '''OUR CODE'''
                    
                    # HAND COORDINATES
                    
                    '''
                    Using depth data of joints - https://github.com/Kinect/PyKinect2/blob/master/pykinect2/PyKinectV2.py
                                                 line: 1816
                                                 
                    Returns a value of the particular joint in relation to the camera.
                    '''
                    
                    left_hand_x = body.joints[PyKinectV2.JointType_HandTipLeft].Position.x;
                    left_hand_y = body.joints[PyKinectV2.JointType_HandTipLeft].Position.y;
                    left_hand_z = body.joints[PyKinectV2.JointType_HandTipLeft].Position.z;
                    
                    right_hand_x = body.joints[PyKinectV2.JointType_HandTipRight].Position.x;
                    right_hand_y = body.joints[PyKinectV2.JointType_HandTipRight].Position.y;
                    right_hand_z = body.joints[PyKinectV2.JointType_HandTipRight].Position.z;  
                    
                    print(type(left_hand_x))
                    
                    left_hand_coordinates = {"visible":"","x":"","y":"","z":""}
                    right_hand_coordinates = {"visible":"","x":"","y":"","z":""}
                    
                    # ROTATION
                    
                    '''
                    Using depth data of shoulder joints to determine rotation.
                    By compareing the z value on players shoulders the rotation is calculated.
                    Small movements do not trigger new events. The previous state must
                    change for an event to trigger as well.
                    '''
                    
                    right_shoulder_z = body.joints[PyKinectV2.JointType_ShoulderRight].Position.z;
                    left_shoulder_z = body.joints[PyKinectV2.JointType_ShoulderLeft].Position.z;
                    #print(f"rightshoulder {right_shoulder_z} leftshoulder {left_shoulder_z}")
                    diff_shoulders = left_shoulder_z - right_shoulder_z
                    
                    if (abs(diff_shoulders) < 0.15):
                        self._current_rotation = "facing table"
                    elif(diff_shoulders < 0):
                        self._current_rotation = "facing left"
                    else:
                        self._current_rotation = "facing right"
                    
                    if (self._current_rotation != self._previous_rotation):
                        print("new rotation detected")
                        self._previous_rotation = self._current_rotation
                        
                        # self.worker.enQueue(data_out)
                        # add hand coord
                        
                    # HAND STATE
                    
                    '''
                    Tracking hand data - https://github.com/Kinect/PyKinect2/blob/master/pykinect2/PyKinectV2.py
                                       - https://docs.microsoft.com/en-us/previous-versions/windows/kinect/dn799273%28v%3dieb.10%29
                    Possible states:
                                     Unknown    =    0
                                     NotTracked =    1
                                     Open       =    2
                                     Closed     =    3
                                     Lasso      =    4
                                     
                    The logic below only tracks if the players hands are opened or closed
                    '''
                    
                    self._left_hand_state = body.hand_left_state
                    self._right_hand_state = body.hand_right_state
                    
                    if((self._right_hand_state == 2) or (self._right_hand_state == 3)):
                        if(self._right_hand_state != self._previous_right_hand_state):
                            if(self._right_hand_state == 2):
                                # hand open
                                print("right hand state changed")
                                self._previous_right_hand_state = self._right_hand_state
                            else:
                                # hand closed
                                continue
                            
                            # self.worker.enQueue(data_out)
                            
                    if(self._left_hand_state == 2 or self._left_hand_state == 3):
                        if(self._left_hand_state != self._previous_left_hand_state):
                            if(self._left_hand_state == 2):
                                # hand open                               
                                print("left hand state changed")
                                self._previous_left_hand_state = self._left_hand_state
                            else:
                                # hand closed
                                continue
                            
                            # self.worker.enQueue(data_out)
                            # add hand coord
                    
                    
                    ''' OTHERS CODE '''
                    joints = body.joints
                    # convert joint coordinates to color space 
                    joint_points = self._kinect.body_joints_to_color_space(joints)
                    
                    self.draw_body(joints, joint_points, SKELETON_COLORS[i])

            # --- copy back buffer surface pixels to the screen, resize it if needed and keep aspect ratio
            # --- (screen size may be different from Kinect's color frame size) 
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


__main__ = "Kinect v2 Body Game"
client_id = "DummyClient"
client = mqtt.Client(client_id)
# set username and pw to MQTT broker and connect
client.username_pw_set("twzdgqki", "aB6nkIbUQ7Nx")
client.connect('m24.cloudmqtt.com', 13583, 60)
url='http://10.2.5.219:8080/shot.jpg' #Filips telefon

stopper = threading.Event()
wThread = worker("Worker-thread",stopper, client)
wThread.start()
mThread = imageFeed(url, "Marker-thread", wThread, stopper)
mThread.start()
game = BodyGameRuntime("Kinect-thread",wThread,stopper);
game.run();
mThread.join()   #Väntar på att tråden ska bli klar!
wThread.join()
print("Threads done")