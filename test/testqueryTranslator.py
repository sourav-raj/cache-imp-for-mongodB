# -*- coding: utf-8 -*-
# Indentation: Visual Studio

'''
creating db and storing result to table.

'''


__version__ = "0.0.1"
__author__ = "Sourav Raj"
__author_email__ = "souravraj.iitbbs@gmail.com"

import json
import sys

sys.path.append('./')

from src.parser.queryTranslator import QueryTranslator


jsonFile=r'G:\bits\sem2\Systems for data analytics\Assignment\data\queries.json'
f = open(jsonFile)
queries=json.load(f)
query=''
selectedFields, filter= None, None
qt=QueryTranslator('test')

for query_ in queries['queries']:
    query=query_['query']
    query=qt.mongoDbToSqlQueryParser(query)
    print(query)

