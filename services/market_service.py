import os
import magic
import base64
from bson import Binary
from werkzeug.utils import secure_filename
from db import mongo
from models.market import get_market_collection

UPLOAD_FOLDER = 'uploads/images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def add_pokemon_to_market(data, logged_in_user_id):
    try:
        image_data = data['image']
        if isinstance(image_data, bytes):
            image_binary = image_data
            image_content_type = 'application/unknown-image-type'
        else:
            if not image_data:
                raise ValueError("No image file uploaded.")
            filename = secure_filename(image_data.filename)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            image_data.save(image_path)
            with open(image_path, 'rb') as f:
                image_binary = f.read()
            mime = magic.Magic(mime=True)
            image_content_type = mime.from_file(image_path)

        pokemon = {
            'name': data['name'],
            'description': data['description'],
            'price': data['price'],
            'stats': data['iv_stats'],
            'image': {
                'data': Binary(image_binary),
                'contentType': image_content_type
            },
            'user_id': logged_in_user_id
        }

        market_collection = get_market_collection()
        market_collection.insert_one(pokemon)

        return {'message': 'Pokémon added to market successfully.'}, 201
    except Exception as e:
        return {'message': str(e)}, 400

def get_all_pokemons_in_market():
    try:
        market_collection = get_market_collection()
        pokemons = list(market_collection.find())
        for pokemon in pokemons:
            pokemon["_id"] = str(pokemon["_id"])
            if isinstance(pokemon.get('image'), dict):
                image_data = pokemon['image'].get('data')
                if image_data:
                    encoded_image = base64.b64encode(image_data).decode('utf-8')
                    pokemon['image'] = {
                        'data': encoded_image,
                        'contentType': pokemon['image'].get('contentType')
                    }
                else:
                    pokemon['image'] = None
            else:
                pokemon['image'] = None
            if 'stats' in pokemon:
                pokemon['stats'] = pokemon['stats'] if isinstance(pokemon['stats'], dict) else eval(pokemon['stats'])
        return {'message': 'Pokémons retrieved successfully', 'pokemons': pokemons}, 200
    except Exception as e:
        return {'message': str(e)}, 400
