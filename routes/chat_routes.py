from flask import Blueprint, Response, jsonify
from flask_cors import CORS
from services.chat_service import authorize_request, connected_users as get_connected_users

chat_bp = Blueprint('chat', __name__, url_prefix='/dmx')
CORS(chat_bp)

@chat_bp.route('/cmds', methods=['GET'])
def index():
    user_id = authorize_request()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    return jsonify({'message': 'Chat Backend Running', 'user_id': user_id})


@chat_bp.route('/connected-users', methods=['GET'])
def connected_users():
    user_id = authorize_request()
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
        
    return jsonify({
        'connected_users': get_connected_users(),
        'count': len(get_connected_users())
    })