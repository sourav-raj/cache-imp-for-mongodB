# -*- coding: utf-8 -*-
# Indentation: Visual Studio

'''
Building Cache for MongoDB

'''

__version__ = "0.0.1"
__author__ = "Sourav Raj"
__author_email__ = "souravraj.iitbbs@gmail.com"

import sys
import pymongo
import json
from decimal import Decimal
from bson.decimal128 import Decimal128, create_decimal128_context
sys.path.append('./')
from tqdm import tqdm as TQ
from time import time

from src.common.config import QUERIESFILE, MONGODBURL, MONGODATABASENAME, MONGODBCOLLECTIONNAME, SQLITEDBFILE, SQLITETABLENAME, SQLITETABLECOLUMNS
from src.parser.queryTranslator import QueryTranslator
from src.localStorage.localStorage import LocalStorage
from src.mongoDB.mongoDBConnector import MongoDB

sql_create_projects_table = f""" CREATE TABLE IF NOT EXISTS {SQLITETABLENAME} (
                                _id integer PRIMARY KEY,
                                name text, 
                                summary text,
                                description text,
                                neighborhood_overview text,
                                property_type text,
                                room_type text,
                                bed_type text,
                                minimum_nights text,
                                maximum_nights text,
                                cancellation_policy text,
                                accommodates interger,
                                bedrooms integer,
                                beds integer,
                                number_of_reviews integer,
                                bathrooms real,
                                price real,
                                security_deposit real,
                                cleaning_fee real,
                                extra_people real,
                                guests_included integer                                   
                                ); """

# D128_CTX = create_decimal128_context()
QUERIESFILE=r'G:\bits\sem2\Systems for data analytics\Assignment\data\queriesSample.json'
queries=json.load(open(QUERIESFILE))
qt=QueryTranslator(SQLITETABLENAME)
localStorage=LocalStorage(SQLITEDBFILE)
conn = localStorage.create_connection()
localStorage.createTable(sql_create_projects_table)
mongoDB=MongoDB(MONGODBURL, MONGODATABASENAME, MONGODBCOLLECTIONNAME)
mongoDB.createConnection()

def dataFormator(record:dict, tableColumns:list=SQLITETABLECOLUMNS):
    data=[]
    for column in tableColumns:
        if record.get(column):
            if column in  ['bathrooms', 'price', 'security_deposit', 'cleaning_fee', 'extra_people', 'guests_included']:
                data.append(float(record.get(column).to_decimal()))
            else: data.append(record.get(column))
        else: data.append(None)
    return tuple(data)


for query_ in queries['queries']:
    mongoDBquery=query_['query']
    print(mongoDBquery)
    sqlQuery=qt.mongoDbToSqlQueryParser(mongoDBquery)
    print(sqlQuery)
    records=[]
    start_time=time()
    records=localStorage.fetchData(sqlQuery)
    if records:
        print(f'data is fetched from cache(local storage) with 1st record _id  is: {records[0][0]} & it took {time()-start_time}')
    elif ' or ' in sqlQuery.split('where')[1]:
        # print(sqlQuery.split('where')[1], 'dssda')
        for individualFilter in sqlQuery.split('where')[1].split(' or '):
            individualQuery = sqlQuery.split('where')[0] + ' where ' + individualFilter
            print(individualQuery)
            records.append(localStorage.fetchData(sqlQuery))
        if records:
            print(f'data is fetched from cache(local storage) with 1st record _id  is: {records[0][0]} & it took {time()-start_time}')
    else:
        print(f"no data is found for the query {mongoDBquery}")
        records=mongoDB.fetchData(mongoDBquery)
        print(f'data is fetched from mongoDB & it took {time()-start_time}')
        for record in TQ(records, desc="Local storage - data insertion"):
            # print(record)
            data=dataFormator(record)
            # print(data)
            localStorage.insertData(SQLITETABLENAME, data)
        print('data is inserted')