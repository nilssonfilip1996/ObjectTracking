# -*- coding: utf-8 -*-
"""
Created on Sun May 19 11:35:23 2019
Simple client for verifying that a MQTT client receives data correctly
Uses CloudMQTT.
@author: Filip Nilsson & Aron Polner
"""
# import libraries
import json
import paho.mqtt.client as mqtt

# Event callback. Triggered when a new event is received by the broker.
def on_message(mosq, obj, msg):
    data_recv=json.loads(msg.payload)
    print(data_recv)

if __name__ == '__main__':
    client_id = "Simple_client"
    # create client object
    client = mqtt.Client(client_id)   
    # assign event callbacks
    client.on_message = on_message  
    # set username and pw to MQTT broker and connect
    client.username_pw_set("user", "password")      #<--Change to actual credentials
    client.connect('m24.cloudmqtt.com', "port", 60) #<--Change to actual credentials
    # start asynchronous loop an subscribe
    client.loop_start()
    client.subscribe("tracking_data",0) 
    #To exit the program, press a key
    input("press a button to exit the simple client.")
    
    