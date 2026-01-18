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
        self._save_lobby(lobby)

        return {
            'lobby_code': key,
            'host_id': host.id
        }

    def join_lobby(self, code: str, username: str, avatar: str, user_id: Optional[str]) -> dict:
        """Add new user to an existing lobby"""
        lobby: Lobby = self._get_lobby(code)

        # If user_id is provided and user exists in lobby, handle reconnection
        if user_id and user_id in lobby.users:
            existing_user = lobby.users[user_id]
            # If username matches, it's a reconnection - return existing user
            if existing_user.username == username:
                return {
                    'user_id': existing_user.id
                }
            # If username changed, check if new username is available
            # (excluding the current user from the check)
            if any(user.username == username and user.id != user_id for user in lobby.users.values()):
                raise ValueError('Username is taken')
            # Update username and avatar for reconnecting user
            existing_user.username = username
            existing_user.avatar = avatar
            self._save_lobby(lobby)
            return {
                'user_id': existing_user.id
            }

        # Check if username is taken for new users
        lobby.is_username_taken(username)

        # Create and add user to lobby (with provided user_id if given, otherwise generate new)
        user = User(username, avatar, user_id)
        lobby.add_user(user)

        # Save to Redis
        self._save_lobby(lobby)

        return {
            'user_id': user.id
        }
    
    def game_start(self, code: str, user_id: str):
        lobby: Lobby = self._get_lobby(code)
        if user_id != lobby.host_id:
            raise ValueError("User is not the host")
        lobby.start_game()
        self._save_lobby(lobby)
        # TODO: return game state and emit socket to each user with their roles(must not be shown in chat)

    def perform_night_action(self, code: str, user_id: str, target_username: Optional[str] = None):
        """Perform a night action. Validates user and role, then calls role's perform_night_action."""
        lobby: Lobby = self._get_lobby(code)
        
        # Validate game is in night phase
        if lobby.game_state != 'night':
            raise ValueError("Game is not in night phase")
        
        # Get user and validate they exist
        if user_id not in lobby.users:
            raise ValueError("User not found in lobby")
        
        user = lobby.users[user_id]
        if not user.alive:
            raise ValueError("User is not alive")
        
        if not user.role:
            raise ValueError("User has no role assigned")
        
        # Call the role's perform_night_action - role handles its own validation
        result = user.role.perform_night_action(lobby, user_id, target_username)
        
        # Save to Redis after action
        self._save_lobby(lobby)
        
        return result

    """ Voting """
    async def begin_vote(self, code: str):
        lobby: Lobby = self._get_lobby(code)
        lobby.votes, lobby.user_vote = setup_vote(lobby.remaining_players)
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
        leading_username = get_leading_vote(lobby.votes)
        # Check if saved (future roles)
        if leading_username:
            # Find user_id from username
            target_user_id = None
            for uid, user in lobby.users.items():
                if user.username == leading_username:
                    target_user_id = uid
                    break
            if target_user_id:
                lobby.eliminate(target_user_id)
        # Save to Redis
        self._save_lobby(lobby)

    def cast_vote(self, code: str, voter_id: str, target_username: str):
        """Cast a vote using functional approach. Returns current vote state."""
        
        lobby: Lobby = self._get_lobby(code)
        # Validate target is alive
        if target_username not in lobby.remaining_players:
            raise ValueError("Invalid target")
        # Validate killer can't vote another killer at night
        if lobby.game_state == 'night':
            if target_username in lobby.killers:
                raise ValueError("Can't kill a killer")
        
        # Remove previous vote if exists
        if voter_id in lobby.user_vote.keys():
            prev_target = lobby.user_vote[voter_id]
            lobby.votes[prev_target] -= 1
        
        # Add new vote
        lobby.user_vote[voter_id] = target_username
        lobby.votes[target_username] += 1
        
        # Check if voting is complete
        is_complete = False
        eliminated_username = None
        
        # Get eligible voters count
        if lobby.game_state == 'day':
            eligible_voters = len(lobby.remaining_players)
        elif lobby.game_state == 'night':
            # Count active killers using property
            eligible_voters = len(lobby.active_killers)
        else:
            eligible_voters = 0
        
        # Check for majority or all voted
        majority_username = check_majority(eligible_voters, lobby.votes)
        if majority_username or all_voted(eligible_voters, len(lobby.user_vote)):
            is_complete = True
            # Use majority result if available, otherwise get leading vote
            leading_username = majority_username or get_leading_vote(lobby.votes)
            if leading_username:
                # Find user_id from username for eliminate
                target_user_id = None
                for uid, user in lobby.users.items():
                    if user.username == leading_username:
                        target_user_id = uid
                        break
                if target_user_id:
                    lobby.eliminate(target_user_id)
                    eliminated_username = leading_username
        
        # Save to Redis
        self._save_lobby(lobby)
        
        # Return vote state for broadcasting
        return {
            "votes": {username: count for username, count in lobby.votes.items() if count > 0},
            "user_votes": lobby.user_vote.copy(),
            "is_complete": is_complete,
            "eliminated_username": eliminated_username
        }