from flask import Blueprint, jsonify, request
from flask_cors import CORS
from services.pokemon_seeder import spawn_random_pokemon
from routes.auth_routes import require_sign_in
from db import mongo
from bson import ObjectId

pokemon_spawner_bp = Blueprint('pokemon_spawner', __name__, url_prefix='/pokemon_spawner')

CORS(pokemon_spawner_bp)

def convert_objectid_to_str(pokemon):
    if isinstance(pokemon, dict):
        return {key: str(value) if isinstance(value, ObjectId) else convert_objectid_to_str(value) 
                for key, value in pokemon.items()}
    elif isinstance(pokemon, list):
        return [convert_objectid_to_str(item) if isinstance(item, dict) else item for item in pokemon]
    return pokemon

@pokemon_spawner_bp.route('/spawn', methods=['POST'])
@require_sign_in
def spawn():
    pokemon_data, status = spawn_random_pokemon()

    if status != 200:
        return jsonify({"error": "Failed to generate Pokemon"}), status
    
    user_id = request.user['_id']
    pokemon_data["user_id"] = user_id

    mongo.db.pokemons.insert_one(pokemon_data)

    pokemon_data = convert_objectid_to_str(pokemon_data)

    return jsonify(pokemon_data), 201
