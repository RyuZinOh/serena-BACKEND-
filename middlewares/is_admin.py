from functools import wraps
from flask import request, jsonify
import jwt
from config import Config
from db import mongo
from bson import ObjectId
from flask_cors import CORS

def is_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        token = token.replace("Bearer ", "")
        
        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('sub')
            if not user_id:
                return jsonify({'message': 'User ID missing in token'}), 400

            user_collection = mongo.db.users
            user = user_collection.find_one({'_id': ObjectId(user_id)})

            if not user:
                return jsonify({'message': 'User not found!'}), 404

            if user.get('role') != 1:
                return jsonify({'message': 'Permission denied! Admins only.'}), 403

            return f(*args, **kwargs)
        
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401
        except Exception as e:
            return jsonify({'message': str(e)}), 500

    return decorated_function
