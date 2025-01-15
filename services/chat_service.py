from flask import request
from extensions import socketio
from services.user_service import decode_token

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

    print(f"Message received from {user_id}: {data}")
    socketio.emit('message', {'text': data['text'], 'timestamp': data['timestamp'], 'sender': data['sender'], 'channel': data['channel']})
