from pymongo import MongoClient

class MongoDB:
    def __init__(self, db_uri, db_name):
        self.client = MongoClient(db_uri)
        self.db_name = db_name
        self.db = self.client[db_name]
        print("Connected to MongoDB Atlas!")

    def close(self):
        self.client.close()
        print("MongoDB connection closed.")

    def get_collection(self, collection_name):
        return self.db[collection_name]
    
    def ping_db(self):
        print(self.client.list_database_names())

    def find(self, collection, params):
        return self.db[collection].find(params)
    
    def find_one(self, collection_name, params):
        return self.db[collection_name].find_one(params)
    
    def insert_one(self, collection_name, params):
        return self.db[collection_name].insert_one(params)
    
    def insert_many(self, collection_name, params):
        return self.db[collection_name].insert_many(params)
    