import traceback
import logging
import json
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from flask_socketio import SocketIO, emit

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": ["http://localhost", "https://localhost"]}})

socketio = SocketIO(app, cors_allowed_origins=["http://localhost", "https://localhost"])

MESSAGES_FILE = 'messages.json'

def initialize_messages_file():
    try:
        with open(MESSAGES_FILE, 'x') as file:
            json.dump([], file)
    except FileExistsError:
        pass
    except Exception as e:
        print(f"Error initializing messages file: {e}")

initialize_messages_file()

@app.route('/api/message', methods=['POST'])
def handle_message():
    try:
        logging.debug(f"Request headers: {request.headers}")
        logging.debug(f"Request data: {request.data}")

        message = request.get_json(force=True)
        logging.debug(f"Parsed message: {message}")

        if not message or not isinstance(message, dict):
            return {'error': 'Invalid JSON payload. Expected a JSON object.'}, 400

        with open(MESSAGES_FILE, 'r') as file:
            try:
                messages = json.load(file)
                logging.debug(f"Loaded messages: {messages}")
                if not isinstance(messages, list):
                    logging.error("Messages file contains non-list data. Reinitializing...")
                    messages = []
            except json.JSONDecodeError as e:
                logging.error(f"Error loading JSON from file: {e}")
                return {'error': 'Failed to read messages file'}, 500

        messages.append(message)

        with open(MESSAGES_FILE, 'w') as file:
            json.dump(messages, file, indent=4)

        socketio.emit('new_message', message)

        return {'message': 'Message received and broadcasted'}, 201

    except Exception as e:
        logging.error(f"Error handling message: {e}")
        logging.error(f"Full traceback: {traceback.format_exc()}")
        return {'error': 'An unexpected error occurred'}, 500
    
@app.route('/api/message', methods=['GET'])
def get_messages():
    try:
        with open(MESSAGES_FILE, 'r') as file:
            messages = json.load(file)
            if not isinstance(messages, list):
                messages = []
        return jsonify(messages), 200
    except Exception as e:
        logging.error(f"Error retrieving messages: {e}")
        return {'error': 'An unexpected error occurred'}, 500

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
