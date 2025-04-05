from flask import request
from extensions import socketio
from services.user_service import decode_token
from db import mongo
from flask_socketio import join_room, leave_room, emit
from bson.objectid import ObjectId
from collections import defaultdict

# track connected users 
connected_users = {}
user_socket_map = {}  

def authorize_request():
    token = request.headers.get('Authorization')
    if not token or not token.startswith('Bearer '):
        return None
    return decode_token(token.split(' ')[1])

def get_user_name(user_id):
    """Get user name from DB with proper ObjectId conversion"""
    try:
        if user := mongo.db.users.find_one({"_id": ObjectId(user_id)}, {'name': 1}):
            return user.get('name')
    except:
        pass
    return None

def get_all_connected_users():
    """Return simplified list of connected users {id: name}"""
    return {uid: data['name'] for uid, data in connected_users.items()}

@socketio.on('connect')
def on_connect():
    user_id = authorize_request()
    if not user_id:
        return False

    socket_id = request.sid
    user_socket_map[socket_id] = user_id

   
    if user_id not in connected_users:
        if name := get_user_name(user_id):
            connected_users[user_id] = {
                'name': name,
                'sockets': set()
            }
   
    connected_users[user_id]['sockets'].add(socket_id)
    
   
    if len(connected_users[user_id]['sockets']) == 1:
        join_room('connected_users')
        emit('user_connected', {
            'user_id': user_id,
            'name': connected_users[user_id]['name'],
            'connected_users': get_all_connected_users()
        }, room='connected_users')
        
        print(f"User connected: {connected_users[user_id]['name']} ({user_id})")
        print(f"All connected: {get_all_connected_users()}")

@socketio.on('disconnect')
def on_disconnect():
    socket_id = request.sid
    if socket_id not in user_socket_map:
        return

    user_id = user_socket_map.pop(socket_id)
    
    if user_id not in connected_users:
        return
        

    connected_users[user_id]['sockets'].discard(socket_id)
    

    if len(connected_users[user_id]['sockets']) == 0:
        name = connected_users.pop(user_id)['name']
        leave_room('connected_users')
        
        emit('user_disconnected', {
            'user_id': user_id,
            'name': name,
            'connected_users': get_all_connected_users()
        }, room='connected_users')
        
        print(f"User disconnected: {name} ({user_id})")
        print(f"Remaining users: {get_all_connected_users()}")

@socketio.on('message')
def handle_message(data):
    socket_id = request.sid
    if socket_id not in user_socket_map:
        return False
        
    user_id = user_socket_map[socket_id]
    if user_id not in connected_users:
        return False

    emit('message', {
        'text': data['text'],
        'timestamp': data['timestamp'],
        'sender': connected_users[user_id]['name'],
        'sender_id': user_id,
    }, broadcast=True)
    
    print(f"Message from {connected_users[user_id]['name']}: {data['text']}")

@socketio.on('get_connected_users')
def send_connected_users():
    socket_id = request.sid
    if socket_id not in user_socket_map:
        return
        
    user_id = user_socket_map[socket_id]
    emit('connected_users_list', get_all_connected_users(), room=socket_id)