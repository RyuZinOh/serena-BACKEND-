from flask import Blueprint, Response, request, jsonify
from flask_cors import CORS

from services.user_service import (
    register_user,
    login_user,
    handle_forgot_password,
    upload_profile_picture,
    get_profile_picture,
    delete_profile_picture,
)


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





## CRUD FOR userpfp's
@user_bp.route('/uploadpfp', methods=['POST'])
def upload_pfp():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Authorization token is required.'}), 400

    image_file = request.files.get('file')
    
    if not image_file:
        return jsonify({'message': 'No file part'}), 400

    response, status = upload_profile_picture(image_file, token)
    return jsonify(response), status



@user_bp.route('/mypfp', methods=['GET'])
def get_pfp():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Authorization token is required.'}), 400

    response = get_profile_picture(token)
    if isinstance(response, Response):
        return response
    else:
        return jsonify(response), 404


# @user_bp.route('/updatepfp', methods=['PUT'])
# def update_pfp():
#     token = request.headers.get('Authorization')
#     if not token:
#         return jsonify({'message': 'Authorization token is required.'}), 400

#     image_file = request.files.get('file')
    
#     if not image_file:
#         return jsonify({'message': 'No file part'}), 400

#     response, status = update_profile_picture(image_file, token)
#     return jsonify(response), status

@user_bp.route('/deletepfp', methods=['DELETE'])
def delete_pfp():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Authorization token is required.'}), 400

    response, status = delete_profile_picture(token)
    return jsonify(response), status