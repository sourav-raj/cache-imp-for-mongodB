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


class LocalStorage:

    def __init__(self, db_file):
        self.db_file=db_file

    def create_connection(self):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        self.conn = None
        try:
            self.conn = sqlite3.connect(self.db_file)
            return self.conn
        except Error as e:
            print(e)

        return self.conn

    def createTable(self, createTableSQL):

        """ create a table from the createTableSQL statement
        parameters:
        ----------
            param self: instance
            param createTableSQL: str
            
        Returns:
        -------
             None
        """
        if self.conn is not None:
            try:
                c = self.conn.cursor()
                c.execute(createTableSQL)
            except Error as e:
                print(e)
        else:
            print("Error! cannot create the database connection.")

    def insertData(self, tableName, data):
        """
    
        parameters:
        ----------
            param self: instance
            param tableName: str
            param data: tuple/list of tuple
            
        Returns:
        -------
             None

        """
        sql = f"INSERT INTO {tableName}(id, name) VALUES(?,?)"
        print(sql)
        cur = self.conn.cursor()
        if type(data)==list:
            cur.executemany(sql, data)
        else:
            cur.execute(sql, data)
        self.conn.commit()

        print('We have inserted', cur.rowcount, 'records to the table.')

    def fetchData(self, query):
        """
        parameters:
        ----------
            param self: instance
            param query: str

        Returns:
        -------
             records:list

        """
        # sqlite_select_query = """SELECT * from SqliteDb_developers"""
        cur = self.conn.cursor()
        cur.execute(query)
        records = list(cur.fetchall())
        cur.close()
        return records




    
    