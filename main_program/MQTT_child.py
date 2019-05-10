# MQTT child module

# import libraries
import time
import random
import json
import paho.mqtt.client as mqtt
from pymongo import MongoClient
import threading
import queue

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
    #print("hej")


# event callback
def on_message(mosq, obj, msg):
    data_recv=json.loads(msg.payload)
    # here we can handle recieved data
    #logToDB({"hey":"då"})
    wThread.enQueue(data_recv)
    #print(data_recv)

    
class worker(threading.Thread):
    def __init__(self, name, stopper):
        threading.Thread.__init__(self)
        self._queue = queue.Queue(maxsize=0)
        self.name = name                    #Thread name
        self.stopper = stopper
        
    def run(self):
        print ("Starting " + self.name)
        while not self.stopper.is_set():
            res = self.deQueue()
            if(res!=None):
                print("Work found!")
                self.processContent(res)
            time.sleep(0.1)
        print ("Exiting " + self.name)
        
    def enQueue(self, li):
        self._queue.put(li)
    
    def deQueue(self):
        if(not self._queue.empty()):
            val = self._queue.get()
            self._queue.task_done()
            return val
        else:
            return None
        
    def processContent(self, contentDict):
        print(contentDict)
        client = MongoClient("mongodb+srv://testUser:testUser@el01-cluster-j4gp3.gcp.mongodb.net/test?retryWrites=true")
        db = client.get_database('El01V2')
        collection = db.get_collection(self.colName)
        collection.insert_one(contentDict)
        
    def setCollectionName(self):
        client = MongoClient("mongodb+srv://testUser:testUser@el01-cluster-j4gp3.gcp.mongodb.net/test?retryWrites=true")
        db = client.get_database('El01V2')
        colList = sorted(db.list_collection_names())
        nextColIndex = str(int(colList[-1]) + 1)
        #nextCol = 'markerdata' + str(nextColIndex)
        self.colName = nextColIndex
        print(self.colName)
        
stopper = threading.Event()
wThread = worker("worker-Thread-client",stopper)
wThread.setCollectionName()
#wThread.processContent({"start":"start"})
wThread.start()
if __name__ == '__main__':
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
    
#    wThread.processContent({"då":"hej"})
    
    # only needed to keep the script alive
    run = True
    #wThread.setDaemon(True)
    input("press a button to exit dummy script.")
    #wThread.processContent({"end":"end"})
    stopper.set()
    wThread.join()