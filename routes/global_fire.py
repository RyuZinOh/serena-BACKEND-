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
metadata_url = "https://raw.githubusercontent.com/RyuZinOh/static-assets/main/metadata.json"
response = requests.get(metadata_url)
metadata = response.json()

backgrounds_list = metadata['backgrounds']
cards_list = metadata['cards']

def fetch_images(base_url, image_list):
    """Fetch image data using pre-loaded metadata."""
    return [{"name": image_name, "url": f"{base_url}{image_name}"} for image_name in image_list]

# Backgrounds route
@kamehameha_bp.route('/background', methods=['GET'])
def list_backgrounds():
    backgrounds = fetch_images(BACKGROUND_BASE_URL, backgrounds_list)
    return jsonify({"message": "Backgrounds retrieved successfully", "backgrounds": backgrounds}), 200

# Specific background route
@kamehameha_bp.route('/background/<image_name>', methods=['GET'])
def get_background(image_name):
    url = f"{BACKGROUND_BASE_URL}{image_name}"
    return fetch_image(url)

# Cards route
@kamehameha_bp.route('/card', methods=['GET'])
def list_cards():
    cards = fetch_images(CARD_BASE_URL, cards_list)
    return jsonify({"message": "Cards retrieved successfully", "cards": cards}), 200

# Specific card route
@kamehameha_bp.route('/card/<image_name>', methods=['GET'])
def get_card(image_name):
    url = f"{CARD_BASE_URL}{image_name}"
    return fetch_image(url)

def fetch_image(url):
    try:
        response = requests.get(url, stream=True, timeout=5)
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', 'image/jpeg')
            return Response(response.content, content_type=content_type)
        else:
            return jsonify({"message": "Image not found."}), 404
    except Exception as e:
        return jsonify({"message": f"Error fetching image: {str(e)}"}), 500
