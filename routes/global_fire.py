from flask import Blueprint, jsonify
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
    get_specific_title
)
from flask_cors import CORS

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