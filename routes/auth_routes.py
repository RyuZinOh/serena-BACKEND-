from flask import Blueprint, request, jsonify
from functools import wraps
import jwt
from config import Config
from db import mongo
from bson import ObjectId
from middlewares.is_admin import is_admin
from flask import Blueprint, request, jsonify
from flask_cors import CORS

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
CORS(auth_bp)

def require_sign_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            token = token.replace("Bearer ", "")
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('sub')
            if not user_id:
                return jsonify({'message': 'User ID missing in token'}), 400
            
            user_collection = mongo.db.users
            user = user_collection.find_one({'_id': ObjectId(user_id)})

            if not user:
                return jsonify({'message': 'User not found!'}), 404

            request.user = user
            return f(*args, **kwargs)
        
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401
        except Exception as e:
            return jsonify({'message': str(e)}), 500

    return decorated_function

@auth_bp.route('/user-auth', methods=['GET'])
@require_sign_in
def user_auth():
    user = request.user
    return jsonify({
        'ok': True,
        'user': {
            'id': str(user['_id']),
            'name': user['name'],
            'email': user['email'],
            'phone': user['phone'],
            'address': user['address']
        }
    }), 200

@auth_bp.route('/admin-auth', methods=['GET'])
@require_sign_in
@is_admin
def admin_auth():
    user = request.user
    return jsonify({
        'ok': True,
        'admin': {
            'id': str(user['_id']),
            'name': user['name'],
            'email': user['email'],
            'phone': user['phone'],
            'address': user['address']
        }
    }), 200
