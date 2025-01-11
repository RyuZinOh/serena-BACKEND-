import random
from bson import ObjectId
from flask import jsonify
import requests
from db import mongo


def convert_objectid_to_str(pokemon):
    if isinstance(pokemon, dict):
        return {key: str(value) if isinstance(value, ObjectId) else convert_objectid_to_str(value) 
                for key, value in pokemon.items()}
    elif isinstance(pokemon, list):
        return [convert_objectid_to_str(item) if isinstance(item, dict) else item for item in pokemon]
    return pokemon

def generate_random_iv():
    return {stat: random.randint(0, 31) for stat in ["hp", "attack", "defense", "special_attack", "special_defense", "speed"]}

def spawn_random_pokemon():
    random_id = random.randint(1, 898)
    url = f"https://pokeapi.co/api/v2/pokemon/{random_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        name = data['name'].capitalize()
        types = [t['type']['name'].capitalize() for t in data['types']]
        iv = generate_random_iv()
        sprite = data['sprites']['front_default']
        
        pokemon = {
            "name": name,
            "types": types,
            "sprite": sprite,
            "iv": iv
        }

        return {"message": "Random Pokemon spawned successfully!", "pokemon": pokemon}, 200
    else:
        return {"error": "Failed to fetch data from PokeAPI."}, 500

def delete_pokemon_from_db(pokemon_id, user_id):
    if not ObjectId.is_valid(pokemon_id):
        return jsonify({"error": "Invalid Pokémon ID!"}), 400

    result = mongo.db.pokemons.delete_one({"_id": ObjectId(pokemon_id), "user_id": user_id}) # type: ignore
    if result.deleted_count > 0:
        return jsonify({"message": "Pokémon deleted successfully!"}), 200
    else:
        return jsonify({"error": "Pokémon not found or does not belong to the user!"}), 404

def get_user_pokemons_from_db(user_id):
    cursor = mongo.db.pokemons.find({"user_id": user_id})
    user_pokemons_list = [convert_objectid_to_str(pokemon) for pokemon in cursor]
    return jsonify(user_pokemons_list), 200