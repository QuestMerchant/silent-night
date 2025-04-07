from flask import Flask, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit, join_room, leave_room
from redis_service import GameService

app = Flask(__name__, static_folder='dist', static_url_path='')
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize Redis
game_service = GameService()

# Requires Vue app to be built
@app.route('/')
@app.route('/<path:path>')
def serve_vue(path='index.html'):
    return send_from_directory(app.static_folder, path)

@app.route('/create_lobby', methods=['POST'])
def create_lobby():
    data = request.json
    username = data.get('username')
    game_service.create_lobby(username)
    return jsonify()

@app.route('join_lobby', methods=['POST'])
def join_lobby():
    data = request.json
    username = data.get('username')
    code = data.get('code')

    return jsonify()
