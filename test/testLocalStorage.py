# -*- coding: utf-8 -*-
# Indentation: Visual Studio

'''
test sqllite db connection 

'''

__version__ = 1.0
__author__ = "Sourav Raj"
__author_email__ = "souravraj.iitbbs@gmail.com"

import sys

sys.path.append('./')

from src.localStorage.localStorage import LocalStorage

dbfile=r'G:\bits\sem2\Systems for data analytics\Assignment\data\testsqlite.db'

sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS test (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    property_type text,
                                    
                                ); """


localStorage=LocalStorage(dbfile)
conn = localStorage.create_connection()
localStorage.createTable(sql_create_projects_table)
record=(2, 'Sourav')
localStorage.insertData('test', record)
records = [(1, 'Sambit'), (3, 'Rabi')]
localStorage.insertData('test', records)

query = """SELECT * from test"""
records=localStorage.fetchData(query)
print(f'total records found is {len(records)}')
for _ in records: print(_)
# conn.commit()
conn.close()


