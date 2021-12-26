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

from src.common.config import QUERIESFILE, MONGODBURL, MONGODATABASENAME, MONGODBCOLLECTIONNAME, SQLITEDBFILE, SQLITETABLENAME, \
    SQLITETABLECOLUMNS, logFile
from src.parser.queryTranslator import QueryTranslator
from src.localStorage.localStorage import LocalStorage
from src.mongoDB.mongoDBConnector import MongoDB


sql_create_projects_table = f""" CREATE TABLE IF NOT EXISTS {SQLITETABLENAME} (
                                    query txt PRIMARY KEY NOT NULL,
                                    insertTime timestamp,
                                    accessTime timestamp,
                                    data txt                                
                                ); """

# D128_CTX = create_decimal128_context()
# QUERIESFILE=r'G:\bits\sem2\Systems for data analytics\Assignment\data\queriesSample.json'
queries=json.load(open(QUERIESFILE))
qt=QueryTranslator(SQLITETABLENAME)
localStorage=LocalStorage(SQLITEDBFILE)
conn = localStorage.create_connection()
localStorage.createTable(sql_create_projects_table)
mongoDB=MongoDB(MONGODBURL, MONGODATABASENAME, MONGODBCOLLECTIONNAME)
mongoDB.createConnection()
logger= open(logFile,"a")

def updateAccessTime(records):
    for record in records:
        # print('dsdas', record[0])
        updateQuery=f'UPDATE {SQLITETABLENAME} SET accessTime = {time()} WHERE query = "{record[0]}"'
        # print('fdfd', updateQuery)
        localStorage.updateData(updateQuery)
        # print(updateQuery)

log_=f'********* Cache Building for MongoDB ********* \n\n'
logger.write(log_)
print(log_)

for index, query_ in enumerate(queries['queries']):
   
    mongoDBquery=query_['query']
    # print(mongoDBquery)
    sqlQuery=qt.mongoDbToSqlQueryParser(mongoDBquery)
    start_time=time()
    cacheQuery=f'{sqlQuery.split("where")[0].strip()} where query=  "{sqlQuery.split("where")[1].strip()}"'
    # print(sqlQuery, cacheQuery)
    records=localStorage.fetchData(cacheQuery)
    if records:
        updateAccessTime(records)
        log_=f'Hit: For Query{index+1} data is fetched from cache(local storage) & it took {time()-start_time} \n'
        logger.write(log_)
        print(log_)
    elif ' or ' in sqlQuery.split('where')[1]:
        # print(sqlQuery.split('where')[1], 'dssda')
        records_=[]
        for individualFilter in sqlQuery.split('where')[1].split(' or '):
            individualQuery = f'{sqlQuery.split("where")[0].strip()} where query= "{individualFilter.strip()}"'
            # print(individualQuery)
            record=localStorage.fetchData(individualQuery)
            if record: 
                updateAccessTime(record)
                records_.append(record)
        if records_:
            log_=f'Hit: For Query{index+1} data is fetched from cache(local storage) & it took {time()-start_time} \n'
            logger.write(log_)
            print(log_)
    else:
        # print(f"no data is found for the query {mongoDBquery}")
        records=mongoDB.fetchData(mongoDBquery)
        log_=f'Miss: For Query{index+1}, data is fetched from mongoDB & it took {time()-start_time} \n'
        logger.write(log_)
        print(log_)
        records_=[record for record in list(records)]
        data=(sqlQuery.split('where')[1].strip(), time(), time(), str(records_))
        
        cacheLimit=localStorage.fetchData(f"""SELECT count(*) from {SQLITETABLENAME} """)[0][0]
        # print(cacheLimit)
        if cacheLimit<=2:
            localStorage.insertData(SQLITETABLENAME, data)
        else:
            query = f"""SELECT query from {SQLITETABLENAME} ORDER BY accessTime desc limit 1"""
            lruQuery=localStorage.fetchData(query)[0][0]
            log_=f'For Query{index+1} insertion, Cache Limit exceeds. LRU Implementation : cache with query= "{lruQuery.strip()}" got evicted \n'
            logger.write(log_)
            print(log_)
            deleteQuery=f'DELETE FROM {SQLITETABLENAME} WHERE query= "{lruQuery.strip()}"'
            localStorage.deleteData(deleteQuery)
            localStorage.insertData(SQLITETABLENAME, data)
            

logger.write("\n")
logger.close()