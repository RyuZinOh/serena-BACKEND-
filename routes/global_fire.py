from flask import Blueprint, jsonify, request, send_file
from services.currency_service import get_user_currency
from services.profiling_comps import (
    merge_metadata,
    get_titles,
    BACKGROUND_BASE_URL,
    CARD_BASE_URL,
    backgrounds_data,
    cards_data,
    backgrounds_list,
    cards_list,
    get_background_by_name,
    get_card_by_name,
    get_specific_title,
    get_title_by_id,
    get_json_bg,
    get_json_card,
    generate_profile_image
)
from flask_cors import CORS
from db import mongo
import jwt
from config import Config
import datetime
from services.user_service import decode_token

# Create the Blueprint and enable CORS
kamehameha_bp = Blueprint('kamehameha', __name__, url_prefix='/kamehameha')
CORS(kamehameha_bp)

def create_item_response(base_url, predefined_data, metadata_list, item_type):
    return jsonify({
        "message": f"{item_type.capitalize()} retrieved successfully",
        item_type: merge_metadata(base_url, predefined_data, metadata_list)
    }), 200

#as a whole
@kamehameha_bp.route('/background', methods=['GET'])
def list_backgrounds():
    return create_item_response(BACKGROUND_BASE_URL, backgrounds_data, backgrounds_list, "backgrounds")

@kamehameha_bp.route('/card', methods=['GET'])
def list_cards():
    return create_item_response(CARD_BASE_URL, cards_data, cards_list, "cards")

@kamehameha_bp.route('/title', methods=['GET'])
def list_titles():
    return jsonify({
        "message": "Titles retrieved successfully",
        "titles": get_titles()
    }), 200

#single
@kamehameha_bp.route('/background/<background_name>', methods=['GET'])
def get_specific_background(background_name):
    return get_background_by_name(background_name)

@kamehameha_bp.route('/card/<card_name>', methods=['GET'])
def get_specific_card(card_name):
    return get_card_by_name(card_name)


@kamehameha_bp.route('/title/<int:title_id>', methods=['GET'])
def get_specific_title_route(title_id):
    return get_specific_title(title_id)





#buying implementation
@kamehameha_bp.route('/buy_title/<int:title_id>', methods=['POST'])
def buy_title(title_id):
    token = request.headers.get('Authorization', "").replace("Bearer ", "")
    if not token:
        return jsonify({'message': 'Token is missing!'}), 401

    try:
        decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token.get('sub')
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return jsonify({'message': 'Invalid or expired token!'}), 401

    user_currency = get_user_currency(user_id)
    if not user_currency or user_currency.get("coin_value") <= 0:
        return jsonify({'message': 'Insufficient currency!'}), 400

    title = get_title_by_id(title_id)
    if not title:
        return jsonify({'message': 'Title not found!'}), 404

    title_price = title.get('price', 0)
    if user_currency.get("coin_value") < title_price:
        return jsonify({'message': f'Insufficient currency! Required: {title_price}, Available: {user_currency.get("coin_value")}'}), 400

    mongo.db.p_title.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "user_name": decoded_token.get('name'),
                "title_id": title_id,
                "title_name": title['name'],
                "purchased_at": datetime.datetime.now()
            }
        },
        upsert=True
    )

    mongo.db.currency.update_one({"user_id": user_id}, {"$inc": {"serenex_balance": -title_price}})

    return jsonify({'message': 'Title purchased successfully!'}), 200





@kamehameha_bp.route('/buy_background/<background_name>', methods=['POST'])
def buy_background(background_name):
    token = request.headers.get('Authorization', "").replace("Bearer ", "")
    if not token:
        return jsonify({'message': 'Token is missing!'}), 401

    try:
        decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token.get('sub')
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return jsonify({'message': 'Invalid or expired token!'}), 401

    user_currency = get_user_currency(user_id)
    if not user_currency or user_currency.get("coin_value") <= 0:
        return jsonify({'message': 'Insufficient currency!'}), 400

    background_info = get_json_bg(background_name)
    if not background_info:
        return jsonify({'message': 'Background not found!'}), 404

    background_price = background_info.get('price', 0)
    if user_currency.get("coin_value") < background_price:
        return jsonify({'message': f'Insufficient currency! Required: {background_price}, Available: {user_currency.get("coin_value")}'}), 400

    background_url = background_info['url']

    mongo.db.p_bg.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "user_name": decoded_token.get('name'),
                "background_url": background_url,
                "purchased_at": datetime.datetime.now()
            }
        },
        upsert=True  
    )

    mongo.db.currency.update_one({"user_id": user_id}, {"$inc": {"serenex_balance": -background_price}})

    return jsonify({'message': 'Background purchased successfully!'}), 200

@kamehameha_bp.route('/buy_card/<card_name>', methods=['POST'])
def buy_card(card_name):
    token = request.headers.get('Authorization', "").replace("Bearer ", "")
    if not token:
        return jsonify({'message': 'Token is missing!'}), 401

    try:
        decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token.get('sub')
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired!'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token!'}), 401

    user_currency = get_user_currency(user_id)
    if not user_currency or user_currency.get("coin_value") <= 0:
        return jsonify({'message': 'Insufficient currency!'}), 400

    card_info = get_json_card(card_name)
    if not card_info:
        return jsonify({'message': 'Card not found!'}), 404

    card_price = card_info.get('price', 0)
    if user_currency.get("coin_value") < card_price:
        return jsonify({'message': f'Insufficient currency! Required: {card_price}, Available: {user_currency.get("coin_value")}'}), 400

    card_url = card_info['url']

    mongo.db.p_card.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "user_name": decoded_token.get('name'),
                "card_url": card_url,
                "purchased_at": datetime.datetime.now()
            }
        },
        upsert=True 
    )

    mongo.db.currency.update_one({"user_id": user_id}, {"$inc": {"serenex_balance": -card_price}})

    return jsonify({'message': 'Card purchased successfully!'}), 200


#profile viewing
@kamehameha_bp.route('/profile', methods=['GET'])
def profile():
    token = request.headers.get('Authorization', "").replace("Bearer ", "")
    if not token:
        return jsonify({'message': 'Token is missing!'}), 401

    try:
        decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token.get('sub')
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired!'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token!'}), 401

    title_info = mongo.db.p_title.find_one({"user_id": user_id})
    background_info = mongo.db.p_bg.find_one({"user_id": user_id})
    card_info = mongo.db.p_card.find_one({"user_id": user_id})

    profile_data = {
        "username": decoded_token.get('name'),
        "title_name": title_info.get('title_name') if title_info else None,
        "background_url": background_info.get('background_url') if background_info else None,
        "card_url": card_info.get('card_url') if card_info else None
    }

    return jsonify(profile_data), 200


##generating profile 
@kamehameha_bp.route('/generate_profile', methods=['GET'])
def generate_profile():
    token = request.headers.get('Authorization', "").replace("Bearer ", "")
    if not token:
        return jsonify({'message': 'Token is missing!'}), 401

    try:
        decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token.get('sub')
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired!'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token!'}), 401

    title_info = mongo.db.p_title.find_one({"user_id": user_id})
    background_info = mongo.db.p_bg.find_one({"user_id": user_id})
    card_info = mongo.db.p_card.find_one({"user_id": user_id})

    username = decoded_token.get('name')
    title_name = title_info.get('title_name') if title_info else "No Title"
    background_url = background_info.get('background_url') if background_info else None
    card_url = card_info.get('card_url') if card_info else None

    
    img_io = generate_profile_image(token, username, title_name, background_url, card_url)

    return send_file(img_io, mimetype='image/png')