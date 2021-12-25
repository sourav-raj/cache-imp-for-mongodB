'''
mongoDB cloud db (ATLAS) connector & provide the data.

'''

__version__ = "0.0.1"
__author__ = "Sourav Raj"
__author_email__ = "souravraj.iitbbs@gmail.com"

import pymongo

class MongoDB:
    def __init__(self, url:str, db:str, collection:str) -> None:
        self.url=url
        self.db=db
        self.collection= collection

    def createConnection(self):
        self.myclient=pymongo.MongoClient(self.url)
        self.db=self.myclient[self.db]
        self.collection=self.db[self.collection]
        # collection.count_documents({})

    def fetchData(self, query):
        records=self.collection.aggregate(query)
        return records

