from flask import Blueprint, request, jsonify

from services.user_service import (
    register_user,
    login_user,
    handle_forgot_password,
    check_role_from_db,
    add_pokemon,
    list_pokemons,
    update_pokemon,
    delete_pokemon
)


user_bp = Blueprint('user', __name__, url_prefix='/user')

##user section
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


## pokemon section
@user_bp.route('/<user_id>/add-pokemon', methods=['POST'])
def add_pokemon_route(user_id):
    token = request.headers.get('Authorization')
    data = request.get_json()
    response, status = add_pokemon(user_id, data, token)
    return jsonify(response), status

@user_bp.route('/<user_id>/pokemons', methods=['GET'])
def list_pokemons_route(user_id):
    token = request.headers.get('Authorization')
    response, status = list_pokemons(user_id, token)
    return jsonify(response), status

@user_bp.route('/<user_id>/update-pokemon/<pokemon_id>', methods=['PUT'])
def update_pokemon_route(user_id, pokemon_id):
    token = request.headers.get('Authorization')
    data = request.get_json()
    response, status = update_pokemon(user_id, pokemon_id, data, token)
    return jsonify(response), status

@user_bp.route('/<user_id>/delete-pokemon/<pokemon_id>', methods=['DELETE'])
def delete_pokemon_route(user_id, pokemon_id):
    token = request.headers.get('Authorization')
    response, status = delete_pokemon(user_id, pokemon_id, token)
    return jsonify(response), status