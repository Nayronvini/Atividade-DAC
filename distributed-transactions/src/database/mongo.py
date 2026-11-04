from pymongo import MongoClient
from src.core.config import settings

client = MongoClient(settings.mongo_url, serverSelectionTimeoutMS=5000, retryWrites=True)
database = client[settings.mongo_database]
customers = database["customers"]

def initialize_mongo():
    customers.create_index("operation_id")
    customers.create_index([("_id", 1), ("version", 1)])
    client.admin.command("ping")
