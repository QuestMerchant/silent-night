import json
import random
import redis
import string
from game import User, Lobby
from typing import Optional



class GameService:
    r = redis.Redis(host='localhost', port=6379, decode_responses=True) # change to cloud using secret_key.

    def __init__(self, lobby_ttl=3600): # ttl is timeout/expiration in seconds
        self.lobby_ttl = lobby_ttl
        self.active_lobbies: dict[str, Lobby] = {}

    def _get_lobby_key(self, code: str):
        while self.r.exists(f"lobby: {code}"):
            code = self._generate_code()
        return code
    
    def _generate_code(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    
    def _get_lobby(self, code: str) -> Lobby: 
        # Check memory for lobby
        lobby: Optional[Lobby] = self.active_lobbies.get(code)

        if not lobby:
            # Retrieve lobby from redis
            lobby_data = self.r.get(f"lobby: {code}")
            if lobby_data:
                # Load lobby as instance
                lobby = Lobby.from_dict(json.loads(lobby_data))
                self.active_lobbies[code] = lobby
            else:
                raise ValueError("Lobby not found")
        
        return lobby

    def _save_lobby(self, lobby: Lobby):
        """Save lobby to Redis"""
        self.r.hset(
            f"lobby: {lobby.code}",
            mapping=lobby.to_dict(),
            ex=self.lobby_ttl
        )

    def create_lobby(self, host_name: str, host_avatar: str):
        """Create new lobby with a host user"""
        host = User(host_name, host_avatar)
        code = self._generate_code()
        key = self._get_lobby_key(code)
        lobby = Lobby(host, key)

        # Store instance in memory
        self.active_lobbies[lobby.code] = lobby

        # Save to redis
        self._save_lobby()

        return {
            'lobby_code': key,
            'host_id': host.id
        }

    def join_lobby(self, code: str, username: str, avatar: str) -> dict:
        """Add new user to an existing lobby"""
        lobby: Lobby = self._get_lobby(code)

        # Check if username is taken
        lobby.is_username_taken(username)

        # Create and add user to lobby
        user = User(username, avatar)
        lobby.add_user(user)

        # Save to Redis
        self._save_lobby()

        return {
            'user_id': user.id
        }