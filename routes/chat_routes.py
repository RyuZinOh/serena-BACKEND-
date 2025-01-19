from flask import Blueprint, Response, jsonify
from flask_cors import CORS
from services.chat_service import authorize_request, get_public_profile_picture

chat_bp = Blueprint('chat', __name__, url_prefix='/dmx')
CORS(chat_bp)

@chat_bp.route('/cmds', methods=['GET'])
def index():
    user_id = authorize_request()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    return jsonify({'message': 'Chat Backend Running', 'user_id': user_id})


#getting pfp for user using ids
@chat_bp.route('/pfx/<user_id>', methods=['GET'])
def get_pfp_by_id(user_id):
    image_data = get_public_profile_picture(user_id)
    if not image_data:
        return jsonify({'message': 'No profile picture found.'}), 404

    return Response(image_data, content_type="image/jpeg")




## yet to to add the users 
# global userprofile grabber
# for the message pfp for distinction to seperalty 
# show each user pf who messaged, for now front end is handling the code based on header so only one 
# userpfp is shown everywhere per device