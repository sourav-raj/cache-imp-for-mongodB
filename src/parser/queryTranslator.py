# -*- coding: utf-8 -*-
# Indentation: Visual Studio

'''
creating db and storing result to table.

'''
import sqlite3
from sqlite3 import Error


__version__ = "0.0.1"
__author__ = "Sourav Raj"
__author_email__ = "souravraj.iitbbs@gmail.com"

def fieldDictFilterToSQL(val, key):
    SqlFilter=''
    if isinstance(val, dict):
        if list(val.keys())[0]=='$regex':
            SqlFilter=f"{key} like  '%{list(val.values())[0]}%'"

    else:
        SqlFilter=f"{key} == '{val}'"

    return SqlFilter

class QueryTranslator:

    def __init__(self, tableName) -> None:
        self.tableName=tableName
        self.filter='where '
        self.selectedFields='*'

    def mongoDbToSqlQueryParser(self, query:dict):
        self.filter='where '
        self.selectedFields='*'

        match=query[0]['$match']
        # try:
        #     projection=query[1]['$project']
        #     self.selectedFields = ', '.join([key  for (key, value) in projection.items() if value == 1])
        # except:
        #     print(f'projection is not mentioned, will fetch all the fields')
    
        for key, values_ in match.items():
            if key in ['$or', '$and']:
            # [{'property_type': 'House'}]
            # [{'name': {'$regex': 'Beach'}}, {'property_type': 'House'}]
                for i, val in enumerate(values_):
                    if i<len(values_)-1:
                        self.filter=self.filter + f"{ fieldDictFilterToSQL(list(val.values())[0], list(val.keys())[0])} {key[1:] } " + ' '
                    else:
                        self.filter=self.filter + f"{ fieldDictFilterToSQL(list(val.values())[0], list(val.keys())[0]) }"
            else:
                #{'name': {'$regex': 'Beach'}}, #{'property_type': 'House'}
                self.filter=self.filter + f"{fieldDictFilterToSQL(values_, key)}"

        return f"select {self.selectedFields} from {self.tableName} {self.filter}"
