import requests
from flask import Blueprint, jsonify, Response
from flask_cors import CORS

# Initialize Blueprint
kamehameha_bp = Blueprint('kamehameha', __name__, url_prefix='/kamehameha')
CORS(kamehameha_bp)

# Base URLs for images
BACKGROUND_BASE_URL = "https://raw.githubusercontent.com/RyuZinOh/static-assets/main/Backgrounds/"
CARD_BASE_URL = "https://raw.githubusercontent.com/RyuZinOh/static-assets/main/Cards/"

# Fetch metadata from GitHub
predefined_data_url = "https://raw.githubusercontent.com/RyuZinOh/static-assets/main/marketofserena_predefined_datas.json"
metadata_url = "https://raw.githubusercontent.com/RyuZinOh/static-assets/main/metadata.json"

predefined_data_response = requests.get(predefined_data_url)
metadata_response = requests.get(metadata_url)

predefined_data = predefined_data_response.json()
metadata = metadata_response.json()

backgrounds_data = predefined_data.get('backgrounds', {})
cards_data = predefined_data.get('cards', {})

backgrounds_list = metadata.get('backgrounds', [])
cards_list = metadata.get('cards', [])

def merge_metadata(base_url, predefined_data, all_images):
    """Merge predefined data with all images from metadata.json."""
    images = []
    for image_name in all_images:
        details = predefined_data.get(image_name, ["Description yet to be added.", "Price yet to be added."])
        description = details[0] if len(details) > 0 else "Description yet to be added."
        price = details[1] if len(details) > 1 else "Price yet to be added."
        images.append({
            "name": image_name,
            "url": f"{base_url}{image_name}",
            "description": description,
            "price": price
        })
    return images

# Backgrounds route
@kamehameha_bp.route('/background', methods=['GET'])
def list_backgrounds():
    backgrounds = merge_metadata(BACKGROUND_BASE_URL, backgrounds_data, backgrounds_list)
    return jsonify({"message": "Backgrounds retrieved successfully", "backgrounds": backgrounds}), 200

# Specific background route
@kamehameha_bp.route('/background/<image_name>', methods=['GET'])
def get_background(image_name):
    if image_name in backgrounds_list:
        details = backgrounds_data.get(image_name, ["Description yet to be added.", "Price yet to be added."])
        description = details[0] if len(details) > 0 else "Description yet to be added."
        price = details[1] if len(details) > 1 else "Price yet to be added."
        url = f"{BACKGROUND_BASE_URL}{image_name}"
        return jsonify({
            "message": "Background retrieved successfully",
            "name": image_name,
            "url": url,
            "description": description,
            "price": price
        }), 200
    else:
        return jsonify({"message": "Background not found."}), 404

# Cards route
@kamehameha_bp.route('/card', methods=['GET'])
def list_cards():
    cards = merge_metadata(CARD_BASE_URL, cards_data, cards_list)
    return jsonify({"message": "Cards retrieved successfully", "cards": cards}), 200

# # Specific card route
# @kamehameha_bp.route('/card/<image_name>', methods=['GET'])
# def get_card(image_name):
#     if image_name in cards_list:
#         details = cards_data.get(image_name, ["Description yet to be added.", "Price yet to be added."])
#         description = details[0] if len(details) > 0 else "Description yet to be added."
#         price = details[1] if len(details) > 1 else "Price yet to be added."
#         url = f"{CARD_BASE_URL}{image_name}"
#         return jsonify({
#             "message": "Card retrieved successfully",
#             "name": image_name,
#             "url": url,
#             "description": description,
#             "price": price
#         }), 200
#     else:
#         return jsonify({"message": "Card not found."}), 404
