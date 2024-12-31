import requests

BACKGROUND_BASE_URL = "https://raw.githubusercontent.com/RyuZinOh/static-assets/main/Backgrounds/"
CARD_BASE_URL = "https://raw.githubusercontent.com/RyuZinOh/static-assets/main/Cards/"
TITLES_URL = "https://raw.githubusercontent.com/RyuZinOh/static-assets/main/titles.json"
PREDEFINED_DATA_URL = "https://raw.githubusercontent.com/RyuZinOh/static-assets/main/marketofserena_predefined_datas.json"
METADATA_URL = "https://raw.githubusercontent.com/RyuZinOh/static-assets/main/metadata.json"

def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

predefined_data = fetch_data(PREDEFINED_DATA_URL)
metadata = fetch_data(METADATA_URL)
titles = fetch_data(TITLES_URL)

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

def get_title_by_id(title_id):
    return titles.get(str(title_id))
