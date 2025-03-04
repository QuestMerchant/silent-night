from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room
from redis_service import GameService

app = Flask(__name__)
sio = SocketIO(app, cors_allowed_origins="*")

# Initialize Redis
game_service = GameService()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_game', methods=['POST'])
def create_game():
    #TODO
    return

