from bson import ObjectId
from db import mongo
import jwt
from config import Config

def get_user(object_id, token):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        admin_user_id = payload.get('sub')

        user_collection = mongo.db.users
        user = user_collection.find_one({'_id': ObjectId(object_id)})
        if not user:
            return {'message': 'User not found!'}, 404

        user['_id'] = str(user['_id'])
        return {'message': 'User retrieved successfully.', 'user': user}, 200
    except Exception as e:
        return {'message': str(e)}, 500

def get_all_users(token):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        admin_user_id = payload.get('sub')

        user_collection = mongo.db.users
        users = list(user_collection.find())
        for user in users:
            user['_id'] = str(user['_id'])

        return {'message': 'Users retrieved successfully.', 'users': users}, 200
    except Exception as e:
        return {'message': str(e)}, 500

def update_user(object_id, data, token):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        admin_user_id = payload.get('sub')

        user_collection = mongo.db.users
        user = user_collection.find_one({'_id': ObjectId(object_id)})
        if not user:
            return {'message': 'User not found!'}, 404

        update_data = {}
        if 'name' in data:
            update_data['name'] = data['name']
        if 'email' in data:
            update_data['email'] = data['email']
        if 'phone' in data:
            update_data['phone'] = data['phone']
        if 'address' in data:
            update_data['address'] = data['address']
        if 'securityQues' in data:
            update_data['securityQues'] = data['securityQues']
        if 'role' in data:
            update_data['role'] = data['role']

        result = user_collection.update_one({'_id': ObjectId(object_id)}, {'$set': update_data})
        if result.matched_count == 0:
            return {'message': 'User not found or update failed!'}, 404

        return {'message': 'User updated successfully.'}, 200
    except Exception as e:
        return {'message': str(e)}, 500

def delete_user(object_id, token):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        admin_user_id = payload.get('sub')

        user_collection = mongo.db.users
        result = user_collection.delete_one({'_id': ObjectId(object_id)})
        if result.deleted_count == 0:
            return {'message': 'User not found or delete failed!'}, 404

        return {'message': 'User deleted successfully.'}, 200
    except Exception as e:
        return {'message': str(e)}, 500
