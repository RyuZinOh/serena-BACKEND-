import requests
from flask import jsonify

# Constants
BACKGROUND_BASE_URL = "https://raw.githubusercontent.com/RyuZinOh/static-assets/main/Backgrounds/"
CARD_BASE_URL = "https://raw.githubusercontent.com/RyuZinOh/static-assets/main/Cards/"
TITLES_URL = "https://raw.githubusercontent.com/RyuZinOh/static-assets/main/titles.json"
PREDEFINED_DATA_URL = "https://raw.githubusercontent.com/RyuZinOh/static-assets/main/marketofserena_predefined_datas.json"
METADATA_URL = "https://raw.githubusercontent.com/RyuZinOh/static-assets/main/metadata.json"

def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return {}

# Fetch all data in one go
predefined_data = fetch_data(PREDEFINED_DATA_URL)
metadata = fetch_data(METADATA_URL)
titles = fetch_data(TITLES_URL)

# Access relevant parts of the predefined data
backgrounds_data = predefined_data.get('backgrounds', {})
cards_data = predefined_data.get('cards', {})
backgrounds_list = metadata.get('backgrounds', [])
cards_list = metadata.get('cards', [])

def merge_metadata(base_url, predefined_data, all_images):
    return [
        {
            "name": image_name,
            "url": f"{base_url}{image_name}",
            "description": predefined_data.get(image_name, ["Description yet to be added."])[0],
            "price": predefined_data.get(image_name, ["", "Price yet to be added."])[1],
        }
        for image_name in all_images
    ]

def get_titles():
    return titles


# defination of geting single title, card, background
def get_title_by_id(title_id):
    title_data = titles.get(str(title_id))  
    if title_data:
        return {
            "name": title_data[0],
            "id": title_id,
            "price": title_data[1] 
        }
    return None

def get_specific_title(title_id):
    title = get_title_by_id(title_id)
    if title:
        return jsonify({
            "message": "Title retrieved successfully",
            "title": title
        }), 200
    else:
        return jsonify({
            "message": "Title not found",
            "title": None,
            "error": "The specified title does not exist"
        }), 404
    
def get_predefined_items(type_key):
    predefined_items = predefined_data.get(type_key, {})
    item_list = metadata.get(type_key, [])
    
    return merge_metadata(f"{CARD_BASE_URL if type_key == 'cards' else BACKGROUND_BASE_URL}", predefined_items, item_list)


def get_background_by_name(background_name):
    background_name_without_extension = background_name.split('.')[0]
    background_info = next(
        (item for item in merge_metadata(BACKGROUND_BASE_URL, backgrounds_data, backgrounds_list) if item['name'].split('.')[0] == background_name_without_extension),
        None
    )
    
    if background_info:
        return jsonify({
            "message": "Background retrieved successfully",
            "background": background_info
        }), 200
    else:
        return jsonify({
            "message": "Background not found",
            "error": "The specified background does not exist"
        }), 404
    
def get_card_by_name(card_name):
    card_name_without_extension = card_name.split('.')[0]
    card_info = next(
        (item for item in merge_metadata(CARD_BASE_URL, cards_data, cards_list) if item['name'].split('.')[0] == card_name_without_extension),
        None
    )
    
    if card_info:
        return jsonify({
            "message": "Card retrieved successfully",
            "card": card_info
        }), 200
    else:
        return jsonify({
            "message": "Card not found",
            "error": "The specified card does not exist"
        }), 404

