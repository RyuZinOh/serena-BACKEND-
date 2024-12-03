from functools import wraps
from flask import request, jsonify
import jwt
from config import Config
from db import mongo
from bson import ObjectId

def is_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        token = token.replace("Bearer ", "")
        user_id, error_message = decode_token(token)
        if error_message:
            return jsonify({'message': error_message}), 401
        
        user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        if not user:
            return jsonify({'message': 'User not found!'}), 404
        
        if user.get('role') != 1:
            return jsonify({'message': 'Permission denied! Admins only.'}), 403

        return f(*args, **kwargs)

    return decorated_function

def decode_token(token):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        user_id = payload.get('sub')
        if not user_id:
            return None, 'User ID missing in token'
        return user_id, None
    except jwt.ExpiredSignatureError:
        return None, 'Token has expired!'
    except jwt.InvalidTokenError:
        return None, 'Invalid token!'
    except Exception as e:
        return None, str(e)
