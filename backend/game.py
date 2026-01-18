import random
import uuid
import time
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Optional


class Lobby:
    def __init__(self, host: 'User', game_code=None):
        self.code = game_code
        self.host_id = host.id
        host.is_host = True
        self.users: dict[str, 'User'] = {host.id: host}
        self.settings = { # Default settings
            'roles': {
                'Serial Killers': 1,
                'Spies': 0
            },
            'night length': 10,
            'day length': 60
        }
        self.role_map = {
            'Serial Killer': SerialKiller(),
            'Spy': Spy(),
            'Civilian': Civilian()
        }
        self.game_state = 'lobby' # lobby, game started
        self.eliminated = []
        self.remaining_players = [] # list of usernames
        self.remaining_players_number = len(self.remaining_players)
        self.assigned_roles = defaultdict(list) # regular_dict = dict(self.assigned_roles)
        self.votes = {}  # {username: vote_count}
        self.user_vote = {}  # {voter_id: target_username}
    
    @property
    def killers(self):
        """Return list of killer usernames"""
        killer_ids = self.assigned_roles.get('killers', [])
        return [self.users[killer_id].username for killer_id in killer_ids if killer_id in self.users]
    
    @property
    def active_killers(self):
        """Return list of active (alive) killer usernames"""
        return [username for username in self.killers if username in self.remaining_players]
    
    def is_username_taken(self, username):
        if any(user.username == username for user in self.users.values()):
            raise ValueError('Username is taken')

    def add_user(self, user: 'User'):
        if self.game_state != 'lobby':
            raise ValueError('Game is already in progress')
        self.users[user.id] = user

    def remove_user(self, user_id):
        if user_id in self.users:
            del self.users[user_id]

        # If host leaves, pick a new host
        if user_id == self.host_id:
            new_host_id = next(iter(self.users))
            self.users[new_host_id].is_host = True
            self.host_id = new_host_id

    def update_settings(self, settings):
        pass

    def start_game(self):
        """Assign roles, validate users and settings and start game"""
        # Check if there are enough players to fill roles
        total_special_roles = sum(self.settings['roles'].values())
        if len(self.users) < total_special_roles:
            raise ValueError('Not enough players to start the game')
        
        # Make sure there aren't too many killers
        if len(self.users) <= self.settings['Serial Killers'] // 2: # Either killers win immediately or one night occurs and they auto win
            raise ValueError('Too many killers for amount of players')
        
        # Assign roles
        user_ids = list(self.users.keys())
        random.shuffle(user_ids)
        self.assign_roles(user_ids)
        
        # Initialize remaining players list with usernames
        self.remaining_players = [user.username for user in self.users.values()]
        self.remaining_players_number = len(self.remaining_players)

        # Start night phase
        self.game_state = 'night'
        self.night_action_phase()

    def assign_roles(self, user_ids):
        # Fill list of all available roles
        roles = []
        for role, count in self.settings['roles'].items():
            roles.extend([role] * count)
        default_role = 'Civilian'
        remaining = len(user_ids) - len(roles)
        roles.extend([default_role] * remaining)
        # Assign roles from role list
        for i, user_id in enumerate(user_ids):
            self.users[user_id].role = self.create_role(roles[i], user_id)

    """Role Factory"""    
    def create_role(self, role_name, user_id):
        if role_name == 'Serial Killers':
            self.assigned_roles['killers'].append(user_id)
            return self.role_map['Serial Killer']
        elif role_name == 'Spies':
            self.assigned_roles['spies'].append(user_id)
            return self.role_map['Spy']
        else:
            return self.role_map['Civilian']

    def check_win_conditions(self) -> Optional[dict]:
        """Check win conditions for all roles. Returns winning team info or None"""
        # Group users by role to check team win conditions
        role_groups = {}
        for user in self.users.values():
            if user.alive and user.role:
                role_name = user.role.name
                if role_name not in role_groups:
                    role_groups[role_name] = []
                role_groups[role_name].append(user)
        
        # Check win condition for each unique role
        for role_name, users in role_groups.items():
            if users and users[0].role.check_win_condition(self):
                return {
                    "winner": role_name,
                    "team": [user.username for user in users]
                }
        
        return None

    def to_dict(self):
        """Convert Lobby to a dict for storing in memory/Redis"""
        return {
            'code': self.code,
            'host_id': self.host_id,
            'settings': self.settings,
            'game_state': self.game_state,
            'users': { uid: user.to_dict() for uid, user in self.users.items()},
            'remaining_players': self.remaining_players
        }

    @classmethod
    def from_dict(cls, data): # cls refers to the class itself and allowing creating an instance without calling a constructor
        host_id = data['host_id']


    def eliminate(self, user_id):
        user = self.users[user_id]
        user.alive = False
        self.eliminated.append(user.id)
        # Remove username from remaining_players
        # Note: active_killers property will automatically update since it's computed from remaining_players
        if user.username in self.remaining_players:
            self.remaining_players.remove(user.username)

    def new_game(self):
        for user in self.users.values(): 
            self.remaining_players.append(user.username)
            user.reset()
        self.game_state = 'lobby'
        self.assigned_roles = defaultdict(list)



# user.role = roleClass() to assign or user.assign_role(roleClass())
class User:
    def __init__(self, username: str, avatar: str, user_id=None):
        self.username = username
        self.avatar = avatar
        self.id = user_id or str(uuid.uuid4())
        self.alive = True # Alive by default
        self.role = None # Assign at game start
        self.is_host = False # Assign host when creating lobby, only host can change rules

    def assign_role(self, role: 'Role'):
        self.role = role

    def reset(self):
        self.alive = True
        self.role = None

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'alive': self.alive,
            'host': self.is_host,
            'role': self.role
        }


class Role(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def night_action(self, lobby: 'Lobby'):
        pass

    @abstractmethod
    def perform_night_action(self, lobby: 'Lobby', user_id: Optional[str] = None, target_username: Optional[str] = None):
        """Perform the night action. Each role validates its own parameters."""
        pass
    
    @abstractmethod
    def check_win_condition(self, lobby: 'Lobby') -> bool:
        """Check if this role's team has won. Returns True if win condition is met."""
        pass

    def to_dict(self):
        return {
            'name': self.name
        }


class SerialKiller(Role):
    def __init__(self):
        super().__init__('Serial Killer')
        self.visible_to = {'Serial Killer'}
        """ Possible function for visiblity
        def view(viewer):
        for user in users:
            if self.role.name in user.role.visible_to:
                return user.role.name
            else:
                return 'unknown'
                
        Other option, make a dictionary of roles and users in roles('Spy': [user1, user7]), adding to dict as assigning roles to avoid iterating unncessarily
        dict.get(visible_roles)"""
    
    def night_action(self, lobby: 'Lobby'):
        # Voting is handled via functional approach in redis_service
        pass

    def perform_night_action(self, lobby: 'Lobby', user_id: str, target_username: Optional[str] = None):
        """Serial Killer must provide a target_username to vote on killing"""
        if not target_username:
            raise ValueError("Serial Killer must provide a target_username")
        # Find user by username
        target_user = None
        for user in lobby.users.values():
            if user.username == target_username:
                target_user = user
                break
        if not target_user:
            raise ValueError("Invalid target")
        if target_user.username not in lobby.remaining_players:
            raise ValueError("Target is not alive")
        
        # Validate killer can't vote another killer
        if target_username in lobby.killers:
            raise ValueError("Can't kill a killer")
        
        # Voting is handled in redis_service.cast_vote()
        # This method just validates the action is allowed
        return {"success": True, "vote_cast": target_username}
    
    def check_win_condition(self, lobby: 'Lobby') -> bool:
        """Killers win if alive killers >= half of remaining players"""
        return len(lobby.active_killers) >= len(lobby.remaining_players) / 2


class Spy(Role):
    def __init__(self):
        super().__init__('Spy')

    def night_action(self, lobby: 'Lobby'):
        chosen: 'User' = input('Choose a player to investigate')
        self.reveal(chosen)

    def reveal(self, target: 'User'):
        return target.role.name
    
    def perform_night_action(self, lobby: 'Lobby', target_username: Optional[str] = None):
        """Spy must provide a target_username to investigate"""
        if not target_username:
            raise ValueError("Spy must provide a target_username")
        # Find user by username
        target_user = None
        for user in lobby.users.values():
            if user.username == target_username:
                target_user = user
                break
        if not target_user:
            raise ValueError("Invalid target")
        if not target_user.alive:
            raise ValueError("Target is not alive")
        if not target_user.role:
            raise ValueError("Target has no role assigned")
        return {"success": True, "revealed_role": self.reveal(target_user)}
    
    def check_win_condition(self, lobby: 'Lobby') -> bool:
        """Spies win if all killers are eliminated"""
        return len(lobby.active_killers) == 0
    
class Civilian(Role):
    def __init__(self):
        super().__init__('Civilian')

    def night_action(self, lobby: 'Lobby'):
        # send action to sleep
        pass

    def perform_night_action(self, lobby: 'Lobby', target_username: Optional[str] = None):
        """Civilian does nothing at night. target_username should not be provided."""
        if target_username:
            raise ValueError("Civilian cannot perform actions with a target")
        return {"success": True}
    
    def check_win_condition(self, lobby: 'Lobby') -> bool:
        """Civilians win if all killers are eliminated"""
        return len(lobby.active_killers) == 0



