from flask import Blueprint, jsonify
from flask_cors import CORS
from services.chat_service import authorize_request

chat_bp = Blueprint('chat', __name__)
CORS(chat_bp)

@chat_bp.route('/cmds', methods=['GET'])
def index():
    user_id = authorize_request()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    return jsonify({'message': 'Chat Backend Running', 'user_id': user_id})




## yet to to add the users 
# global userprofile grabber
# for the message pfp for distinction to seperalty 
# show each user pf who messaged, for now front end is handling the code based on header so only one 
# userpfp is shown everywhere per device