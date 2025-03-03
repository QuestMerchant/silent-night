from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
import redis

app = Flask(__name__)
sio = SocketIO(app, cors_allowed_origins="*")
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

@app.route('/create_game', methods=['POST'])
def create_game():
    #TODO
    return

