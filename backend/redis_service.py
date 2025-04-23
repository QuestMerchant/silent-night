import json
import random
import redis
import string
import asyncio
from game import User, Lobby
from typing import Optional
from voting import setup_vote, check_majority, get_leading_vote, all_voted, timer



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

    def join_lobby(self, code: str, username: str, avatar: str, user_id: Optional[str]) -> dict:
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
    
    def game_start(self, code: str):
        lobby: Lobby = self._get_lobby(code)
        # TODO
        # Assign roles, emit socket to change to game
        lobby.game_state = 'night'

    """ Voting """
    async def begin_vote(self, code: str):
        lobby: Lobby = self._get_lobby(code)
        lobby.votes, lobby.user_vote, lobby.leading_votes = setup_vote(lobby.remaining_players)
        start_time = asyncio.get_event_loop().time()

        if lobby.game_state == 'day':
            task_timer = asyncio.create_task(timer(lobby.settings['day length']))
            lobby.timer = task_timer 
            await task_timer
            # Finalize vote. Eliminate player, emit result

        elif lobby.game_state == 'night':
            task_timer = asyncio.create_task(timer(lobby.settings['night length']))
            lobby.timer = task_timer 
            await task_timer
            # Finalize outcome
        voted_user = get_leading_vote(lobby.votes)
        # Check if saved (future roles)
        if voted_user:
            lobby.eliminate(voted_user)
        # Save to Redis
        self._save_lobby()

    def cast_vote(self, code: str, voter_id, target_id):
        lobby: Lobby = self._get_lobby(code)
        # Validate target is alive
        if target_id not in lobby.remaining_players:
            raise ValueError("Invalid target")
        # Killers can't vote to kill another killer
        if lobby.game_state == 'night':
            active_killers = [killer for killer in lobby.assigned_roles['killers'] if lobby.users[killer].alive] 
            if target_id in lobby.assigned_roles['killers']:
                raise ValueError("Can't kill a killer")
            
        # Remove existing previous vote
        if voter_id in lobby.user_vote.keys():
            prev_target = lobby.user_vote[voter_id]
            lobby.votes[prev_target] -= 1
        
        # Add new vote
        lobby.user_vote[voter_id] = target_id
        lobby.votes[target_id] += 1

        # Run checks for majority or all voted
        if lobby.game_state == 'day':
            voters = lobby.remaining_players_number
        elif lobby.game_state == 'night':
            voters = len(active_killers)
        if check_majority(voters, lobby.votes) or all_voted(voters, len(lobby.user_vote)):
            task = lobby.timer
            task.cancel()