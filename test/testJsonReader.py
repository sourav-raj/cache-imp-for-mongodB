# -*- coding: utf-8 -*-
# Indentation: Visual Studio

'''
creating db and storing result to table.

'''
import sqlite3
from sqlite3 import Error


__version__ = 1.0
__author__ = "Sourav Raj"
__author_email__ = "souravraj.iitbbs@gmail.com"

import json

def fieldDictFilterToSQL(val, key):
    SqlFilter=''
    if isinstance(val, dict):
        if list(val.keys())[0]=='$regex':
            SqlFilter=f"{key} like  %{list(val.values())[0]}%"

    else:
        SqlFilter=f"{key} == {val}"

    return SqlFilter

jsonFile=r'G:\bits\sem2\Systems for data analytics\Assignment\data\queries.json'
f = open(jsonFile)
queries=json.load(f)
query=''
selectedFields, filter= None, None
for query_ in queries['queries']:
    query=query_['query']
    print(query)

    match=query[0]['$match']
    filter=''
    try:
        projection=query[1]['$project']
        selectedFields = ', '.join([key  for (key, value) in projection.items() if value == 1])
    except:
        print(f'projection is not mentioned, will fetch all the fields')
        selectedFields='*'
   
    for key, values_ in match.items():
        filter=filter+'where '
        if key in ['$or', '$and']:
        # [{'property_type': 'House'}]
        # [{'name': {'$regex': 'Beach'}}, {'property_type': 'House'}]
            for i, val in enumerate(values_):
                if i<len(values_)-1:
                    filter=filter + f"{ fieldDictFilterToSQL(list(val.values())[0], list(val.keys())[0])} {key[1:] } " + ' '
                else:
                    filter=filter + f"{ fieldDictFilterToSQL(list(val.values())[0], list(val.keys())[0]) }"
        else:
            #{'name': {'$regex': 'Beach'}}, #{'property_type': 'House'}
            filter=filter + f"{fieldDictFilterToSQL(values_, key)}"

    print(selectedFields, filter)



                


    # print(match.keys())

    
# [{'$match': {'$or': [{'name': {'$regex': 'Beach'}}, {'property_type': 'House'}]}}, {'$project': {'name': 1, '_id': 1}}]