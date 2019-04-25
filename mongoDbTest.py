# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 09:08:09 2019

@author: nilss
"""

from pymongo import MongoClient
import json

client = MongoClient("mongodb+srv://nilssonfilip:object-tracking@el01-cluster-j4gp3.gcp.mongodb.net")
db = client.get_database('El01')
collection = db.get_collection('markerdata')

mydict = { "name": "John", "address": "Highway 37" }

print(collection.insert_one(mydict))
#for document in collection.find():
#    print(document)