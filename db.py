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



# Replace these with your MongoDB Atlas credentials
#DB_URI = "mongodb+srv://user:pass1234@your_cluster.mongodb.net/test?retryWrites=true&w=majority"
# DB_URI = "mongodb+srv://user:pass123@cluster0.nhps5bk.mongodb.net/?retryWrites=true&w=majority"
# DB_NAME = "bengab"

# Create a MongoClient instance
# client = MongoClient(MONGODB_URI)

# # Create an instance of the MongoDB class with the client
# db = MongoDB(client, MONGODB_DB)

# db.ping_db()



