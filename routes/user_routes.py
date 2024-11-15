from flask import Blueprint, request, jsonify
from flask_cors import CORS 
from services.user_service import register_user, login_user

user_bp = Blueprint('user', __name__, url_prefix='/user')

# CORS REQ verification for routes api
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
