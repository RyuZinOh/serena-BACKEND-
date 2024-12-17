import os
import magic
import base64
from bson import Binary
from werkzeug.utils import secure_filename
from db import mongo
from models.market import get_market_collection
from bson.objectid import ObjectId

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



##defining the buying methos and fucn
def buy_pokemon(pokemon_id, buyer_id):
    try:
        market_collection = mongo.db.market
        user_currency_collection = mongo.db.currency
        user_owned_collection = mongo.db.userOwned

        pokemon = market_collection.find_one({"_id": ObjectId(pokemon_id)})
        if not pokemon:
            return {'message': 'Pokémon not found in market!'}, 404

        pokemon_price = float(pokemon.get("price", 0))
        if pokemon_price <= 0:
            return {'message': 'Invalid Pokémon price!'}, 400

        user_currency = user_currency_collection.find_one({"user_id": buyer_id})
        if not user_currency or user_currency.get("serenex_balance", 0) < pokemon_price:
            return {'message': 'Insufficient balance to buy this Pokémon!'}, 403

        new_balance = user_currency["serenex_balance"] - pokemon_price
        user_currency_collection.update_one(
            {"user_id": buyer_id},
            {"$set": {"serenex_balance": new_balance}}
        )

        pokemon["_id"] = str(pokemon["_id"])
        pokemon["owner_id"] = buyer_id
        user_owned_collection.insert_one(pokemon)

        market_collection.delete_one({"_id": ObjectId(pokemon_id)})

        return {'message': 'Pokémon purchased successfully!'}, 200

    except Exception as e:
        return {'message': str(e)}, 400


##Getting user owend poke fofr custum dashboard of user owned section
def get_user_owned_pokemons(user_id):
    try:
        user_owned_collection = mongo.db.userOwned
        pokemons = list(user_owned_collection.find({"owner_id": user_id}))

        for pokemon in pokemons:
            pokemon["_id"] = str(pokemon["_id"])  

            if "image" in pokemon and isinstance(pokemon["image"], dict):
                image_data = pokemon["image"].get("data")
                if image_data:
                    encoded_image = base64.b64encode(image_data).decode('utf-8')
                    pokemon["image"] = {
                        "data": encoded_image,
                        "contentType": pokemon["image"].get("contentType")
                    }
                else:
                    pokemon["image"] = None

        return {'message': 'Owned Pokémon retrieved successfully!', 'pokemons': pokemons}, 200

    except Exception as e:
        return {'message': str(e)}, 400