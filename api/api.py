from flask import Flask, request
from flask_cors import CORS  # Import CORS
from flask_socketio import SocketIO, emit

app = Flask(__name__)

# CORS for Flask HTTP and WebSocket connections
CORS(app, resources={r"/api/*": {"origins": "https://localhost"}})  # Allow frontend
socketio = SocketIO(app, cors_allowed_origins="https://localhost")  # Allow WebSocket connections

@app.route('/api/data', methods=['POST'])
def post_data():
    new_item = request.json
    # Your POST logic here
    return {'message': 'Item added'}, 201

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('new_message')
def handle_new_message(message):
    print(f"New message: {message}")
    # Broadcast message to all connected clients
    emit('new_message', message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)