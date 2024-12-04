# routes/pokemon_spawner.py
from flask import Blueprint, jsonify
from flask_cors import CORS  
from services.pokemon_seeder import spawn_random_pokemon
from routes.auth_routes import require_sign_in

pokemon_spawner_bp = Blueprint('pokemon_spawner', __name__, url_prefix='/pokemon_spawner')

CORS(pokemon_spawner_bp)  

@pokemon_spawner_bp.route('/spawn', methods=['GET'])
@require_sign_in
def spawn():
    pokemon, status = spawn_random_pokemon()
    return jsonify(pokemon), status
