from flask import request
from extensions import socketio
from services.user_service import decode_token
from db import mongo

def authorize_request():
    token = request.headers.get('Authorization')
    if not token or not token.startswith('Bearer '):
        return None

    token = token.split(' ')[1]
    return decode_token(token)

@socketio.on('connect')
def on_connect():
    user_id = authorize_request()
    if not user_id:
        return False

    print(f"User {user_id} connected")

@socketio.on('message')
def handle_message(data):
    user_id = authorize_request()
    if not user_id:
        return

    socketio.emit('message', {
        'text': data['text'],
        'timestamp': data['timestamp'],
        'sender': data['sender'],
        'sender_id': user_id,

    })

    print(f"Message received from {user_id}: {data}")



def get_public_profile_picture(user_id):
    user_pfp = mongo.db.alluserpfp.find_one({"user_id": user_id})
    if not user_pfp or not user_pfp.get("pfp_file"):
        return None  #
    return user_pfp["pfp_file"]
