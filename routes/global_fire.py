from flask import Blueprint, jsonify, Response, request
from flask_cors import CORS
import requests

kamehameha_bp = Blueprint('kamehameha', __name__, url_prefix='/kamehameha')
CORS(kamehameha_bp)

# Utility function to get all background images
def get_background_images():
    base_url = "https://raw.githubusercontent.com/RyuZinOh/static-assets/main/Backgrounds/"
    supported_extensions = ['jpg', 'jpeg', 'png', 'gif']
    image_list = []

    for i in range(1, 120):  
        for ext in supported_extensions:
            image_name = f"{i}.{ext}"
            image_list.append({
                "name": image_name,
                "url": f"{base_url}{image_name}"
            })

    return image_list

# Utility function to get all card images
def get_card_images():
    base_url = "https://raw.githubusercontent.com/RyuZinOh/static-assets/main/Cards/"
    supported_extensions = ['jpg', 'jpeg', 'png', 'gif']
    image_list = []

    for i in range(1, 46): 
        for ext in supported_extensions:
            image_name = f"{i}.{ext}"
            image_list.append({
                "name": image_name,
                "url": f"{base_url}{image_name}"
            })

    return image_list

# Backgrounds route
@kamehameha_bp.route('/background', methods=['GET'])
def list_backgrounds():
    backgrounds = get_background_images()
    return jsonify({
        "message": "Backgrounds retrieved successfully",
        "backgrounds": backgrounds
    }), 200

# Specific background route
@kamehameha_bp.route('/background/<image_name>', methods=['GET'])
def get_background(image_name):
    base_url = "https://raw.githubusercontent.com/RyuZinOh/static-assets/main/Backgrounds/"
    url = f"{base_url}{image_name}"

    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', 'image/jpeg')
            return Response(response.content, content_type=content_type)
        else:
            return jsonify({"message": "Image not found."}), 404
    except Exception as e:
        return jsonify({"message": f"Error fetching image: {str(e)}"}), 500

# Cards route
@kamehameha_bp.route('/card', methods=['GET'])
def list_cards():
    cards = get_card_images()
    return jsonify({
        "message": "Cards retrieved successfully",
        "cards": cards
    }), 200

# Specific card route
@kamehameha_bp.route('/card/<image_name>', methods=['GET'])
def get_card(image_name):
    base_url = "https://raw.githubusercontent.com/RyuZinOh/static-assets/main/Cards/"
    url = f"{base_url}{image_name}"

    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', 'image/jpeg')
            return Response(response.content, content_type=content_type)
        else:
            return jsonify({"message": "Image not found."}), 404
    except Exception as e:
        return jsonify({"message": f"Error fetching image: {str(e)}"}), 500
