# Object tracking system


## Table of contents
* [General info](#general-information)
* [Dependencies](#dependencies)
* [Setup](#setup)

## General information
A combination of marker tracking technology and depth sensing is used for tracking 2D markers as well as a single player in a tabletop environment. The system categorizes and stores basic events such as placing, removing, and changing the location of a 2D marker as well as logging a player’s rotation in relation to the table.

## Dependencies
* pykinect2 library
* pygame library
* ar_markers library
* threading library
* paho.mqtt.client library
* queue library
* json library
* urllib library
* numpy library
* dictdiffer library
* cv2 library

## Setup
### Hardware
* Kinect V2 for tracking a single player
* An IP-camera without any distortion effects such as fisheye
* A computer to run the program

### Software
All of the necessary files are found in the main\_program folder. The dependencies listed above has to be installed. Before running the system, markers have to be generated. This is done through the ar\_marker\_generator.py module.

#### Configuring the marker tracking subsystem
In order to track the markers, an IP-camera has to be up and running. The IP-address where the camera feed is made available has to be copied and set as the value to the url variable found in the PyKinectBodyTracking\_MainThead\_cleanup.py module.

#### Configuring the player tracking subsystem
In order to track the player, the Kinect V2 SDK has to be installed and the Kinect V2 plugged into the computer.

#### Launching the object tracking system
Having configured the marker and player tracking subsystems, the object tracking system can be launched. This is done by running the PyKinectBodyTracking\_MainThead\_cleanup.py module.
