# 載入 pymongo 套件
from fastapi import Depends
from pymongo import DESCENDING, MongoClient
from pymongo.collection import Collection
# MongoDB 雲端資料庫的網址
mongo_uri = "mongodb+srv://epuie:Ste410119@mycluster.lexggmc.mongodb.net/?retryWrites=true&w=majority"
# 選擇操作 article_system 資料庫
database_name = "article_system"

# Dependency to get the MongoDB database connection
def get_db():
    client = MongoClient(mongo_uri)
    db = client[database_name]
    return db

# Dependency to get the MongoDB collection
def get_collection(db: Collection = Depends(get_db)):
    collection = db["article"]
    return collection
