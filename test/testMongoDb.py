# -*- coding: utf-8 -*-
# Indentation: Visual Studio

'''
Building Cache for MongoDB

'''

__version__ = 1.0
__author__ = "Sourav Raj"
__author_email__ = "souravraj.iitbbs@gmail.com"


import pymongo


if __name__=='__main__':
        url="mongodb+srv://admin:Admin2021@cluster0.mjug9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"    
        myclient = pymongo.MongoClient(url)
        db = myclient["sample_airbnb"]
        collection = db["listingsAndReviews"]
        s = collection.aggregate([
                {"$match" : {
                                "$or" : [
                                        {"name": {"$regex":"Beach"} },
                                        {"property_type":"House"}
                                ]
                }},
                { "$project": { "name": 1, "_id": 0} }
        ])
        count = 0
        for record in s:
            if count<=3: print(record)
            count = count + 1
        print("#records: " + str(count))