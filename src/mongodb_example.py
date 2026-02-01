from pymongo import MongoClient

client = MongoClient(
    "mongodb://root:rootpass@mongodb:27017",
    serverSelectionTimeoutMS=5000,
)

client.admin.command("ping")
print("mongodb: ok")
