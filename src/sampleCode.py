import pymongo

def execute_mongo(url):

        myclient = pymongo.MongoClient(url)
        db = myclient["sample_airbnb"]
        collection = db["listingsAndReviews"]

        # following 2 queries show simple filtering of data with OR condition

        # match with logical operator and counting
        # name contains beach or house type property or accomodates > 6
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
                print(record)
                count = count + 1
        print("#records: " + str(count))

        print("----------")

        s = collection.aggregate([
                {
                        "$match" : {
                                        "$or" : [
                                                {"property_type":"House"}
                                        ]
                        },

                },
                { "$project": { "name": 1, "_id": 0} }
        ])
        count = 0
        for record in s:
                print(record)
                count = count + 1
        print("#records: " + str(count))

        '''

        # some more sample queries

        # match with no logical operator - check for field
        s = collection.aggregate([ 
                {
                        "$match" : {
                                        "name": {"$regex":"Beach"}, 
                                        "property_type": {"$exists":True, "$eq": "House"}, 
                                        "accommodates": {"$gt": 6 }
                                        
                        }

                }, 
                {        
                        "$count":  "number_of_records"  
                }
                 
        ])
        
        # find with logical operator, sort,  selection , limit  
        s =  collection.find( { "$or" : [ {"name":{"$regex":"Beach"} } , { "property_type":"House"} ] }, {"name":1,"_id":0} ).sort("name",-1).limit(10)

        
        # text search
        resp = collection.create_index([ ("name", "text")])
        print("index creation response:", resp)
        s =  collection.find( { "$text" : { "$search" : "beach" } }, {"name":1,"accommodates":1,"_id":0}).sort("accommodates", -1).limit(10)

        # count with group by with filtered rows

        s = collection.aggregate([ 
                {
                        "$match" : {
                                        "$and" : [
                                        {"name": {"$regex":"Beach"} }, 
                                        {"accommodates": {"$gt": 6 }}
                                        ]
                        }
                },

                {
                        "$group" : {
                                        "_id": {
                                                 "property_type": "$property_type"
                                        },
                                        "count":  {"$sum":1} 
                        }
                },
                {
                        "$sort" : { 
                                 "count" : -1
                        }
                }
                 
        ])

        # sort search results by score 
        s = collection.aggregate([ 

                        { "$match": { "$text": { "$search": "beach front" } } },
                        { "$project": { "name": 1, "_id": 0, "score": { "$meta": "textScore" } } },
                        { "$match": { "score": { "$gt": 1.0 } } },
                        { "$sort": { "score": -1}},
                        { "$limit": 10}
                ])
        
        '''

# take url from the mongoDB instance you create
execute_mongo(url)