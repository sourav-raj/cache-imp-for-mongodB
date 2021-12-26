# -*- coding: utf-8 -*-
# Indentation: Visual Studio

'''
Building Cache for MongoDB

'''

__version__ = "0.0.1"
__author__ = "Sourav Raj"
__author_email__ = "souravraj.iitbbs@gmail.com"



QUERIESFILE=r'G:\bits\sem2\Systems for data analytics\Assignment\data\queries.json'


MONGODBURL="mongodb+srv://*****:********@cluster0.mjug9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"    
MONGODATABASENAME='sample_airbnb'
MONGODBCOLLECTIONNAME='listingsAndReviews'

SQLITEDBFILE=r'G:\bits\sem2\Systems for data analytics\Assignment\data\airbnb_sqlite.db'
SQLITETABLENAME='listingsAndReviews'
SQLITETABLECOLUMNS=['queryId', 'query', 'insertTime', 'accessedTime', 'data']
logFile=r'G:\bits\sem2\Systems for data analytics\Assignment\data\log\cache.log'
# SQLITETABLENAME='listingsAndReviews_sqlite'
# SQLITETABLECOLUMNS=["_id", "name", "summary", "description", "neighborhood_overview", "property_type", "room_type", "bed_type", "minimum_nights", "maximum_nights", "cancellation_policy", "accommodates",
# "bedrooms", "beds", "number_of_reviews", "bathrooms", "price", "security_deposit", "cleaning_fee", "extra_people", "guests_included"]



