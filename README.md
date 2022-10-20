
#### Building a cache for MongoDB

Caches are often used to improve database query performance, especially to exploit temporal and spatial locality of user queries. In this assignment, you are expected to build a front-end cache that demonstrates the benefits of caching to improve end user performance of a Cloud hosted MongoDB.

##### Scenario:
The MongoDB instance on Cloud contains an Airbnb dataset with accommodation listing. Users search the database using MongoDB queries. A cache stores the results of the user queries. A user’s MongoDB query is first analyzed by the cache lookup to figure out if it can be served from the local cached data. If the query cannot be served from cache, then it is sent to the Cloud instance which leads to higher overheads. In case of significant cache hits across several queries, the average query response time should improve. 

Let’s take an example. A user query requests for all accommodation names that contain the word “beach” OR the property type is “house”. The query runs on the Cloud instance for the first time. The result of the query is cached with some meta-data to describe the cached data. For e.g. each cache entry’s meta-data captures that the record contains the “name” attribute and the filter condition that matched, i.e. whether the “name” contains “beach” OR “property_type”=”house” OR both. 

This makes it easy to find subset matches in the cache, e.g. all properties of type “house” even if the name doesn’t contain “beach”. Now, when the same or a different user makes a query for properties of type “house”, the query result can be served from the cache because the cache already contains the data for matching accommodations (cache hit). Notice that the query need not be exactly the same and the meta-data helps to find out a subset match. 

The cache lookup logic can find out if the cached data “contains” the result for the new query. The cache lookup logic also needs to be correct to ensure that when data is not in the cache it is a cache miss. For a miss, the query is executed on the Cloud DB and result returned, as well as the cache is updated with data with the appropriate meta-data.


