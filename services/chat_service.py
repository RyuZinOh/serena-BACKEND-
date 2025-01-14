from extensions import socketio

@socketio.on('message')
def handle_message(data):
    print(f"Message received: {data}")
    socketio.emit('message', data)
