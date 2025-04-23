from flask import Flask, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit, join_room, leave_room
from redis_service import GameService
import asyncio

app = Flask(__name__, static_folder='../frontend/dist', static_url_path='')
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
    data: dict = request.json
    username = data.get('name')
    avatar = data.get('avatar')
    try:
        lobby = game_service.create_lobby(username, avatar)
        return jsonify(lobby) # lobby_code : key, host_id: id
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('join_lobby', methods=['POST'])
def join_lobby():
    data: dict = request.json
    username = data.get('username')
    code = data.get('code')
    avatar = data.get('avatar')
    user_id = data.get('userID')
    try:
        lobby = game_service.join_lobby(code, username, avatar, user_id)

        # Send message to lobby
        socketio.emit('user_joined', {
            'name': username
        })
        return jsonify(lobby) # user_id: id
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('start', methods=['POST'])
def start():
    data: dict = request.json
    code = data.get('code')
    game_service.game_start(code)

@app.route('start_day', methods=['POST'])
def start_day():
    data: dict = request.json
    code = data.get('code')
    try:
        asyncio.create_task(game_service.begin_vote(code))
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
