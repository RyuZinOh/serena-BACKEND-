from werkzeug.security import check_password_hash, generate_password_hash
from db import mongo
import datetime
from config import Config
import jwt

def register_user(data):
    name = data['name']
    email = data['email']
    password = data['password']
    phone = data['phone']
    address = data['address']
    securityQues = data['securityQues']
    role = data['role']

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

    user_collection.insert_one(new_user)
    return {'message': 'User registered successfully'}, 201

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
        
        # Create JWT token
        payload = {
            'sub': str(user['_id']),  # subject is the user ID
            'name': user['name'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expiration (1 hour)
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
