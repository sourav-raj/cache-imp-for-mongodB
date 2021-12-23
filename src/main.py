# -*- coding: utf-8 -*-
# Indentation: Visual Studio

'''
Building Cache for MongoDB

'''

__version__ = 1.0
__author__ = "Sourav Raj"
__author_email__ = "souravraj.iitbbs@gmail.com"


import pymongo
import json

jsonFile=r'G:\bits\sem2\Systems for data analytics\Assignment\data\queries.json'
f = open(jsonFile)
queries=json.load(f)
query=''
for query_ in queries['queries']:
    query=query_['query']
    print(query)




url="mongodb+srv://admin:Admin2021@cluster0.mjug9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"    
myclient = pymongo.MongoClient(url)
db = myclient["sample_airbnb"]
collection = db["listingsAndReviews"]

records=collection.aggregate(query)
print(records)

count = 0
for record in records:
        if count <=3:  print(record)
        count = count + 1
print("#records: " + str(count))

# url="mongodb+srv://admin:Admin2021@cluster0.mjug9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"    
# myclient = pymongo.MongoClient(url)
# db = myclient["sample_airbnb"]
# collection = db["listingsAndReviews"]
# collection.count_documents({})