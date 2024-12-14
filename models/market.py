from db import mongo

def get_market_collection():
    return mongo.db.market
