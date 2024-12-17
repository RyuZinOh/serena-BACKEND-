from flask import Blueprint, request, jsonify
from flask_cors import CORS
import jwt
from services.market_service import add_pokemon_to_market, get_all_pokemons_in_market, buy_pokemon, get_user_owned_pokemons
from config import Config
from middlewares.is_admin import is_admin
import os
from werkzeug.utils import secure_filename


market_bp = Blueprint('market', __name__, url_prefix='/market')
CORS(market_bp)

@market_bp.route('/add', methods=['POST'])
@is_admin
def add_market_item():
    try:
        token = request.headers.get('Authorization', "").replace("Bearer ", "")
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        logged_in_user_id = decoded_token.get('sub')

        data = request.form
        required_fields = ['name', 'description', 'price', 'iv_stats']
        if not all(data.get(field) for field in required_fields) or 'image' not in request.files:
            return jsonify({'message': 'Missing required fields or image!'}), 400

        image_file = request.files['image']
        if image_file:
            image_data = image_file.read()

            pokemon_data = {
                'name': data['name'],
                'description': data['description'],
                'price': data['price'],
                'iv_stats': data['iv_stats'],
                'image': image_data
            }

            response, status = add_pokemon_to_market(pokemon_data, logged_in_user_id)
            return jsonify(response), status
        return jsonify({'message': 'Failed to upload image'}), 400
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@market_bp.route('/all', methods=['GET'])
def get_all_market_pokemons():
    try:
        response, status = get_all_pokemons_in_market()
        return jsonify(response), status
    except Exception as e:
        return jsonify({'message': str(e)}), 400



##Buying pkemons for users
@market_bp.route('/buy/<pokemon_id>', methods=['POST'])
def buy_market_item(pokemon_id):
    try:
        token = request.headers.get('Authorization', "").replace("Bearer ", "")
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        buyer_id = decoded_token.get('sub')

        response, status = buy_pokemon(pokemon_id, buyer_id)
        return jsonify(response), status

    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired!'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token!'}), 401
    except Exception as e:
        return jsonify({'message': str(e)}), 400


##explicit user ownes
@market_bp.route('/owned', methods=['GET'])
def get_owned_pokemons():
    try:
        token = request.headers.get('Authorization', "").replace("Bearer ", "")
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token.get('sub')

        response, status = get_user_owned_pokemons(user_id)
        return jsonify(response), status

    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired!'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token!'}), 401
    except Exception as e:
        return jsonify({'message': str(e)}), 400