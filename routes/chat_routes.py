from flask import Blueprint
from flask_cors import CORS
from services.chat_service import handle_message

chat_bp = Blueprint('chat', __name__)
CORS(chat_bp)

@chat_bp.route('/cmds')
def index():
    return "Chat Backend Running"