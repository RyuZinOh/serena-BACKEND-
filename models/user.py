from flask_pymongo import PyMongo

def get_user_collection(mongo: PyMongo):
    return mongo.db.users
