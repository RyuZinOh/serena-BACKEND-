import requests
from flask import Response, jsonify
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import matplotlib.font_manager as fm


from services.user_service import get_profile_picture


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

##using a font matplob library
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

def get_json_bg(background_name):
    background_name_without_extension = background_name.split('.')[0]
    background_info = next(
        (item for item in merge_metadata(BACKGROUND_BASE_URL, backgrounds_data, backgrounds_list) if item['name'].split('.')[0] == background_name_without_extension),
        None
    )
    return background_info


def get_json_card(card_name):
    card_name_without_extension = card_name.split('.')[0]
    card_info = next(
        (item for item in merge_metadata(CARD_BASE_URL, cards_data, cards_list) if item['name'].split('.')[0] == card_name_without_extension),
        None
    )
    return card_info














def generate_profile_image(token, username, title_name, background_url=None, card_url=None, output_format="PNG"):
    canvas_width, canvas_height = 1440, 992
    upper_height = 595
    lower_height = canvas_height - upper_height

    background = Image.new('RGBA', (canvas_width, canvas_height), (255, 255, 255, 255))

    if background_url:
        try:
            bg_image = Image.open(requests.get(background_url, stream=True).raw).convert("RGBA")
            width_percent = (upper_height / float(bg_image.size[1]))
            new_width = int(float(bg_image.size[0]) * width_percent)
            bg_image = bg_image.resize((new_width, upper_height))
            background.paste(bg_image, (0, 0))
        except Exception:
            pass

    draw = ImageDraw.Draw(background)
    draw.line([(0, upper_height), (canvas_width, upper_height)], fill="black", width=2)
    draw.rectangle([(0, upper_height), (canvas_width, canvas_height)], fill="white")

    profile_picture = None
    pfp_response = get_profile_picture(token)
    if isinstance(pfp_response, Response) and pfp_response.status_code == 200:
        profile_picture = pfp_response.get_data()

    if profile_picture:
        try:
            avatar = Image.open(BytesIO(profile_picture)).convert("RGBA").resize((300, 300))
            mask = Image.new('L', avatar.size, 0)
            draw_mask = ImageDraw.Draw(mask)
            draw_mask.ellipse((0, 0, 300, 300), fill=255)
            circular_avatar = Image.new('RGBA', avatar.size)
            circular_avatar.paste(avatar, (0, 0), mask)

            avatar_top_y = upper_height - 150
            background.paste(circular_avatar, (50, avatar_top_y), circular_avatar)
        except Exception:
            pass

    if card_url:
        try:
            card_image = Image.open(requests.get(card_url, stream=True).raw).convert("RGBA").resize((390, 690))
            tilted_card = card_image.rotate(-10, expand=True)
            card_x = 900
            card_y = 94
            background.paste(tilted_card, (card_x, card_y), tilted_card)
        except Exception:
            pass

    try:
        dragon_shadow = Image.open(requests.get("https://github.com/RyuZinOh/static-assets/blob/main/archieved/dragon_shadow.png?raw=true", stream=True).raw).convert("RGBA")
        dragon_shadow = dragon_shadow.resize((150, 150))
        dragon_shadow_x = 50 + (300 - 150) // 2
        dragon_shadow_y = upper_height + 200
        background.paste(dragon_shadow, (dragon_shadow_x, dragon_shadow_y), dragon_shadow)
    except Exception:
        pass

    title_text = title_name if title_name else "N/A"
    username_text = username

    # Use matplotlib to find system fonts
    try:
        font_path = fm.findSystemFonts(fontpaths=None, fontext='ttf')[0]  # Adjust path if necessary
        title_font = ImageFont.truetype(font_path, 40)
        username_font = ImageFont.truetype(font_path, 60)
    except Exception:
        title_font = ImageFont.load_default()
        username_font = ImageFont.load_default()

    draw.text((365, upper_height - 2), username_text, fill="black", font=username_font)
    draw.text((365, upper_height + 50), title_text, fill="black", font=title_font)

    # Convert to RGB mode before saving as JPEG
    if output_format == "JPEG":
        background = background.convert("RGB")  # Convert to RGB to save as JPEG

    img_io = BytesIO()
    background.save(img_io, format=output_format)
    img_io.seek(0)

    return img_io
