from flask_pymongo import PyMongo
from bson import ObjectId
from schemas.user_schema import UserSchema  # Import the schema

# Get the MongoDB user collection
def get_user_collection(mongo: PyMongo):
    return mongo.db.users

# Retrieve user by ID and serialize with schema
def get_user_by_id(mongo: PyMongo, user_id: str):
    user_collection = get_user_collection(mongo)
    user = user_collection.find_one({'_id': ObjectId(user_id)})
    if user:
        user_schema = UserSchema()  # Initialize schema
        return user_schema.dump(user)  # Serialize and return the user data
    return None
