# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 09:08:09 2019

@author: nilss
"""

from pymongo import MongoClient
import json

client = MongoClient("mongodb+srv://nilssonfilip:ekh9lMng@testcluster-m1vgd.gcp.mongodb.net/test?retryWrites=true")
db = client.get_database('test')
collection = db.get_collection('markerdata')

mydict = { "name": "John", "address": "Highway 37" }
collection = db.get_collection('markerdata')
collection.insert_one(mydict)
collection = db.get_collection('markerdata')
for document in collection.find():
    print(document)