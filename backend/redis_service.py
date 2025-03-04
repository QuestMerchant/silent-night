import json
import random
import redis
import string
from game import User, Lobby



class GameService:
    r = redis.Redis(host='localhost', port=6379, decode_responses=True) # change to cloud using secret_key.

    def __init__(self, lobby_ttl=3600): # ttl is timeout/expiration in seconds
        self.lobby_ttl = lobby_ttl

    def _get_lobby_key(self, code):
        while self.r.exists(f"lobby: {code}"):
            code = self._generate_code()
        return code
    
    def _generate_code(self):
        return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=4))
    
    def create_lobby(self, host_name):
        """Create new lobby with a host user"""
        host = User(host_name)
        code = self._generate_code()
        key = self._get_lobby_key(code)
        lobby = Lobby(host, key)

        # Save to redis
        self.r.hset(
            f"lobby: {key}",
            mapping=lobby.to_dict(),
            ex=self.lobby_ttl
        )

        return {
            'lobby_code': key,
            'host_id': host.id
        }