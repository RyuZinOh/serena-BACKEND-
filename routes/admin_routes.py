from flask import Blueprint, request, jsonify
from flask_cors import CORS
from services.admin_manipulator import get_user, get_all_users, update_user, delete_user
from middlewares.is_admin import is_admin

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
CORS(admin_bp)

@admin_bp.route('/user/get_user/<object_id>', methods=['GET'])
@is_admin
def get_user_route(object_id):
    token = request.headers.get('Authorization')
    response, status = get_user(object_id, token)
    return jsonify(response), status

@admin_bp.route('/user/get_all_users', methods=['GET'])
@is_admin
def get_all_users_route():
    token = request.headers.get('Authorization')
    response, status = get_all_users(token)
    return jsonify(response), status

@admin_bp.route('/user/update_user/<object_id>', methods=['PUT'])
@is_admin
def update_user_route(object_id):
    data = request.get_json()
    token = request.headers.get('Authorization')
    response, status = update_user(object_id, data, token)
    return jsonify(response), status

@admin_bp.route('/user/delete_user/<object_id>', methods=['DELETE'])
@is_admin
def delete_user_route(object_id):
    token = request.headers.get('Authorization')
    response, status = delete_user(object_id, token)
    return jsonify(response), status
