# -*- coding: utf-8 -*-
# Indentation: Visual Studio

'''
Building Cache for MongoDB

'''

__version__ = 1.0
__author__ = "Sourav Raj"
__author_email__ = "souravraj.iitbbs@gmail.com"

import sys

sys.path.append('./')

from src.mongoDB.mongoDBConnector import MongoDB




url="mongodb+srv://admin:Admin2021@cluster0.mjug9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"    
db='sample_airbnb'
collection='listingsAndReviews'
mongoDB=MongoDB(url, db, collection)
mongoDB.createConnection()
query = [
        {"$match" : {
                        "$or" : [
                                {"name": {"$regex":"Beach"} },
                                {"property_type":"House"}
                        ]
        }},
        { "$project": { "name": 1, "_id": 1, "property_type": 1} }
]
records=mongoDB.fetchData(query)
count=0
for record in records:
    if count<=3: print(record)
    count = count + 1
print("#records: " + str(count))