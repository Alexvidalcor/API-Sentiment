from pymongo import MongoClient

client = MongoClient("mongodb://localhost/API-Sentiment")

def pickDB(method="Users"):

    db = client.get_database()

    if method =="Users":
        return db["Users"]

    elif method == "Chats":
        return db["Chats"]
