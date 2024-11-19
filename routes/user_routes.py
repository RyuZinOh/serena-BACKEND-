from flask import Blueprint, request, jsonify
from flask_cors import CORS
from services.user_service import register_user, login_user, handle_forgot_password, check_role_from_db

user_bp = Blueprint('user', __name__, url_prefix='/user')
CORS(user_bp)

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    response, status = register_user(data)
    return jsonify(response), status

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    response, status = login_user(data)
    return jsonify(response), status

@user_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    response, status = handle_forgot_password(data)
    return jsonify(response), status

@user_bp.route('/<user_id>/role', methods=['GET'])
def get_user_role(user_id):
    token = request.headers.get('Authorization')
    if not token:
        return {'message': 'Token is missing!'}, 401
    response, status = check_role_from_db(user_id, token)
    return response, status
