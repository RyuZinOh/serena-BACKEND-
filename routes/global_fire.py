from flask import Blueprint, jsonify
from services.profiling_comps import (
    merge_metadata,
    get_titles,
    # get_title_by_id,
    BACKGROUND_BASE_URL,
    CARD_BASE_URL,
    backgrounds_data,
    cards_data,
    backgrounds_list,
    cards_list,
)

kamehameha_bp = Blueprint('kamehameha', __name__, url_prefix='/kamehameha')

@kamehameha_bp.route('/background', methods=['GET'])
def list_backgrounds():
    return jsonify({"message": "Backgrounds retrieved successfully", "backgrounds": merge_metadata(BACKGROUND_BASE_URL, backgrounds_data, backgrounds_list)}), 200

# @kamehameha_bp.route('/background/<image_name>', methods=['GET'])
# def get_background(image_name):
#     if image_name in backgrounds_list:
#         details = backgrounds_data.get(image_name, ["Description yet to be added.", "Price yet to be added."])
#         return jsonify({
#             "message": "Background retrieved successfully",
#             "name": image_name,
#             "url": f"{BACKGROUND_BASE_URL}{image_name}",
#             "description": details[0],
#             "price": details[1]
#         }), 200
#     return jsonify({"message": "Background not found."}), 404

@kamehameha_bp.route('/card', methods=['GET'])
def list_cards():
    return jsonify({"message": "Cards retrieved successfully", "cards": merge_metadata(CARD_BASE_URL, cards_data, cards_list)}), 200

@kamehameha_bp.route('/title', methods=['GET'])
def list_titles():
    return jsonify({"message": "Titles retrieved successfully", "titles": get_titles()}), 200

# @kamehameha_bp.route('/title/<int:title_id>', methods=['GET'])
# def get_title(title_id):
#     title = get_title_by_id(title_id)
#     if title:
#         return jsonify({"message": "Title retrieved successfully", "id": title_id, "title": title}), 200
#     return jsonify({"message": "Title not found."}), 404
