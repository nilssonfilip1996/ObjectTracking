# MQTT child module

# import libraries
import time
import random
import json
import paho.mqtt.client as mqtt
from pymongo import MongoClient

"""
Connect to mongoDB server.
Cluster name: testcluster
Database name: test
Collection name: markerdata
"""
def logToDB(dictContent):
    client = MongoClient("mongodb+srv://nilssonfilip:ekh9lMng@testcluster-m1vgd.gcp.mongodb.net/test?retryWrites=true")
    db = client.get_database('test')
    collection = db.get_collection('markerdata1')
    collection.insert_one(dictContent)
    print("hej")


# event callback
def on_message(mosq, obj, msg):
    data_recv=json.loads(msg.payload)
    # here we can handle recieved data
    logToDB({"hey":"då"})
    print(data_recv)

# building "unique" client ID
current_time = str(time.time()).split(".")
client_id = "DummyClient-" + current_time[0][9:] + \
            current_time[1][:3] + str(random.randint(10,100))

# create client object
client = mqtt.Client(client_id)

# assign event callbacks
client.on_message = on_message

# set username and pw to MQTT broker and connect
client.username_pw_set("twzdgqki", "aB6nkIbUQ7Nx")
client.connect('m24.cloudmqtt.com', 13583, 60)

# start asynchronous loop an subscribe
client.loop_start()
client.subscribe("tracking_data",0)

# only needed to keep the script alive
run = True
while run:
    continue