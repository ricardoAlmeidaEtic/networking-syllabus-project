import traceback
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": ["http://localhost", "https://localhost"]}})

socketio = SocketIO(app, cors_allowed_origins=["http://localhost", "https://localhost"])

messages = []

@app.route('/api/message', methods=['POST'])
def handle_message():
    try:
        logging.debug(f"Request headers: {request.headers}")
        logging.debug(f"Request data: {request.data}")

        message = request.get_json(force=True)
        logging.debug(f"Parsed message: {message}")

        if not message or not isinstance(message, dict):
            return {'error': 'Invalid JSON payload. Expected a JSON object.'}, 400

        messages.append(message)
        socketio.emit('new_message', message)

        return {'message': 'Message received and broadcasted'}, 201

    except Exception as e:
        logging.error(f"Error handling message: {e}")
        logging.error(f"Full traceback: {traceback.format_exc()}")
        return {'error': 'An unexpected error occurred'}, 500
    
@app.route('/api/message', methods=['GET'])
def get_messages():
    try:
        return jsonify(messages), 200
    except Exception as e:
        logging.error(f"Error retrieving messages: {e}")
        return {'error': 'An unexpected error occurred'}, 500

@app.route('/api/message', methods=['PUT'])
def update_message():
    try:
        data = request.get_json()
        message_id = data.get("id")
        new_message = data.get("message")

        if message_id is None or new_message is None:
            return {'error': 'Missing id or message in payload'}, 400

        for message in messages:
            if message.get("id") == message_id:
                message["message"] = new_message
                return {'message': 'Message updated'}, 200

        return {'error': 'Message not found'}, 404
    except Exception as e:
        logging.error(f"Error updating message: {e}")
        return {'error': 'An unexpected error occurred'}, 500

@app.route('/api/message', methods=['DELETE'])
def delete_message():
    try:
        data = request.get_json()
        message_id = data.get("id")

        if message_id is None:
            return {'error': 'Missing id in payload'}, 400

        for message in messages:
            if message.get("id") == message_id:
                messages.remove(message)
                return {'message': 'Message deleted'}, 200

        return {'error': 'Message not found'}, 404
    except Exception as e:
        logging.error(f"Error deleting message: {e}")
        return {'error': 'An unexpected error occurred'}, 500

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
