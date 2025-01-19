from werkzeug.security import check_password_hash, generate_password_hash
from db import mongo
import datetime
from config import Config
import jwt
from bson import ObjectId
import base64
import requests
from bson import Binary
from flask import Response

def register_user(data):
    name = data['name']
    email = data['email']
    password = data['password']
    phone = data['phone']
    address = data['address']
    securityQues = data['securityQues']
    role = 0

    if len(name) < 3 or len(password) < 6:
        return {'message': 'Name must be at least 3 characters and password at least 6 characters.'}, 400

    user_collection = mongo.db.users
    existing_user = user_collection.find_one({'$or': [{'email': email}, {'phone': phone}]})
    if existing_user:
        return {'message': 'Email or phone already exists.'}, 400

    hashed_password = generate_password_hash(password)
    new_user = {
        'name': name,
        'email': email,
        'password': hashed_password,
        'phone': phone,
        'address': address,
        'securityQues': securityQues,
        'role': role
    }

    result = user_collection.insert_one(new_user)
    user_id = str(result.inserted_id)

    initialize_user_currency(user_id)

    return {'message': 'User registered successfully'}, 201


def initialize_user_currency(user_id):
    user_currency = {
        "user_id": user_id,
        "serenex_balance": 100,
        "coin_name": "Serenex"
    }

    mongo.db.currency.insert_one(user_currency)





def login_user(data):
    email = data['email']
    password = data['password']

    user_collection = mongo.db.users
    user = user_collection.find_one({'email': email})

    if user and check_password_hash(user['password'], password):
        user_data = {
            'id': str(user['_id']),
            'name': user['name'],
            'email': user['email'],
            'phone': user['phone'],
            'address': user['address'],
            'securityQues': user['securityQues'],
            'role': user['role']
        }

        payload = {
            'sub': str(user['_id']),
            'name': user['name'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(weeks=1)
        }

        token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
        
        return {'message': 'Login successful', 'user': user_data, 'token': token}, 200
    else:
        return {'message': 'Invalid email or password'}, 401

def handle_forgot_password(data):
    email = data['email']
    securityQues = data['securityQues']
    new_password = data['newPassword']

    user_collection = mongo.db.users
    user = user_collection.find_one({'email': email})

    if not user:
        return {'message': 'User with this email does not exist.'}, 404

    if user['securityQues'] != securityQues:
        return {'message': 'Incorrect security question answer.'}, 400

    hashed_password = generate_password_hash(new_password)
    user_collection.update_one({'email': email}, {'$set': {'password': hashed_password}})
    return {'message': 'Password updated successfully.'}, 200





def decode_token(token):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        return payload.get('sub')
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None





##userpfp serives 

def upload_profile_picture(image_file, token):
    logged_in_user_id = decode_token(token)
    if not logged_in_user_id:
        return {'message': 'Unauthorized!'}, 403

    if not image_file or not allowed_file(image_file.filename):
        return {'message': 'Invalid image file. Only jpg, jpeg, and png are allowed.'}, 400

    try:
        image_data = image_file.read()
        mongo.db.alluserpfp.update_one(
            {"user_id": logged_in_user_id},
            {"$set": {"pfp_file": Binary(image_data)}},
            upsert=True
        )

        return {'message': 'Profile picture uploaded successfully!'}, 201
    except Exception as e:
        return {'message': f'Error uploading image: {str(e)}'}, 500

def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions



def get_profile_picture(token):
    logged_in_user_id = decode_token(token)
    if not logged_in_user_id:
        return {'message': 'Unauthorized!'}, 403

    user_pfp = mongo.db.alluserpfp.find_one({"user_id": logged_in_user_id})
    if not user_pfp or not user_pfp.get("pfp_file"):
        return {'message': 'No profile picture found.'}, 404

    return Response(user_pfp["pfp_file"], content_type="image/jpeg")


def delete_profile_picture(token):
    logged_in_user_id = decode_token(token)
    if not logged_in_user_id:
        return {'message': 'Unauthorized!'}, 403

    try:
        result = mongo.db.alluserpfp.delete_one({"user_id": logged_in_user_id})

        if result.deleted_count == 0:
            return {'message': 'No profile picture found to delete.'}, 404

        return {'message': 'Profile picture deleted successfully!'}, 200
    except Exception as e:
        return {'message': f'Error deleting image: {str(e)}'}, 500
    





