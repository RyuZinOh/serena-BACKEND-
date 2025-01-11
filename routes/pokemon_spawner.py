from flask import Blueprint, jsonify, request
from flask_cors import CORS
from services.pokemon_seeder import convert_objectid_to_str, get_user_pokemons_from_db, spawn_random_pokemon, delete_pokemon_from_db
from db import mongo
from bson import ObjectId
from services.currency_service import get_user_currency
from config import Config
import jwt
from services.user_service import decode_token

pokemon_spawner_bp = Blueprint('pokemon_spawner', __name__, url_prefix='/pokemon_spawner')

CORS(pokemon_spawner_bp)



@pokemon_spawner_bp.route('/spawn', methods=['POST'])
def spawn():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')

    if not token:
        return jsonify({"error": "Authorization token is missing!"}), 401

    user_id = decode_token(token)
    if not user_id:
        return jsonify({"error": "Invalid or expired token!"}), 401

    currency_data = get_user_currency(user_id)
    if not currency_data or currency_data['coin_value'] < 250:
        return jsonify({"error": "Insufficient currency. You need at least 250 to spawn a Pokémon."}), 403

    pokemon_data, status = spawn_random_pokemon()
    if status != 200:
        return jsonify({"error": "Failed to generate Pokémon"}), status

    new_balance = currency_data['coin_value'] - 250
    mongo.db.currency.update_one(
        {"user_id": user_id},
        {"$set": {"serenex_balance": new_balance}}
    )

    pokemon_data["user_id"] = user_id
    mongo.db.pokemons.insert_one(pokemon_data)

    pokemon_data = convert_objectid_to_str(pokemon_data)

    return jsonify(pokemon_data), 201





@pokemon_spawner_bp.route('/user_pokemons', methods=['GET'])
def get_user_pokemons():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return jsonify({"error": "Authorization token is missing!"}), 401

    user_id = decode_token(token)
    if not user_id:
        return jsonify({"error": "Invalid or expired token!"}), 401

    return get_user_pokemons_from_db(user_id)

@pokemon_spawner_bp.route('/delete_pokemon/<string:pokemon_id>', methods=['DELETE'])
def delete_pokemon(pokemon_id):
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return jsonify({"error": "Authorization token is missing!"}), 401

    user_id = decode_token(token)
    if not user_id:
        return jsonify({"error": "Invalid or expired token!"}), 401

    return delete_pokemon_from_db(pokemon_id, user_id)