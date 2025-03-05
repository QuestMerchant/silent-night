import random
import uuid
from abc import ABC, abstractmethod

class Lobby:
    def __init__(self, host: 'User', game_code=None):
        self.code = game_code
        self.host_id = host.id
        host.is_host = True
        self.users = {host.id: host}
        self.settings = { # Default settings
            'Serial Killers': 1,
            'Spies': 0
        }
        self.game_state = 'lobby' # lobby, night, voting/day
        self.eliminated = []
        self.remaining_players = len(self.users) - len(self.eliminated)
    
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
        total_special_roles = sum(self.settings.values())
        if len(self.users) < total_special_roles:
            raise ValueError('Not enough players to start the game')
        
        # Make sure there aren't too many killers
        if len(self.users) <= self.settings['Serial Killers'] // 2: # Either killers win immediately or one night occurs and they auto win
            raise ValueError('Too many killers for amount of players')
        
        # Assign roles
        user_ids = list(self.users.keys())
        random.shuffle(user_ids)
        self.assign_roles(user_ids)

        self.game_state = 'night'

    def assign_roles(self, user_ids): # Figure out a different method to iterate as this will bloat as more roles are added
        # Assign killers
        for i in range(self.settings['Serial Killers']):
            self.users[user_ids[i]].role = SerialKiller()
        # Assign spies
        for i in range(self.settings['Serial Killers'], 
                       self.settings['Serial Killers'] + self.settings['Spies']):
            self.users[user_ids[i]].role = Spy()
        # Assign civilians to remaining users
        for i in range(self.settings['Serial Killers'] + self.settings['Spies'], len(user_ids)):
            self.users[user_ids[i]].assign_role(Civilian())

    """ def assign_roles(self, user_ids):
            # Fill list of all available roles
            roles = []
            for role, count in self.settings.items():
                roles.extend([role] * count) ?
            default_role = 'Civilian'
            remaining = len(user_ids) - len(roles)
            roles.extend([default_role] * remaining)
            # assign roles from list
            """

    def to_dict(self):
        """Convert Lobby to a dict for storing in memory"""
        return {
            'code': self.code,
            'host_id': self.host_id,
            'settings': self.settings,
            'game_state': self.game_state,
            'users': { uid: user.to_dict() for uid, user in self.users.items()},
            'remaining_players': self.remaining_players
        }

    def new_game(self):
        for id, user in self.users.items():
            self.users[id[user]].reset()
        # Alternative, access instance directly, no need for ids as everyone is reset. Also accesses instance method directly 
        # for user in self.users.values(): 
            # user.reset()

# user.role = roleClass() to assign or user.assign_role(roleClass())
class User:
    def __init__(self, username, user_id=None):
        self.username = username
        self.id = user_id or str(uuid.uuid4())
        self.alive = True # Alive by default
        self.role = None # Assign at game start
        self.is_host = False # Assign host when creating lobby, only host can change rules

    def assign_role(self, role: 'Role'):
        self.role = role
    
    def eliminated(self):
        self.alive = False

    def reset(self):
        self.alive = True
        self.role = None

    def to_dict(self):
        return {
            #'id': self.id,
            'username': self.username,
            'alive': self.alive,
            'host': self.is_host,
            'role': self.role
        }
    

class Role(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def night_action(self):
        pass

    def to_dict(self):
        return {
            'name': self.name
        }


class SerialKiller(Role):
    def __init__(self):
        super().__init__('Serial Killer')
        self.visible_to = ['Serial Killer']
    
    def night_action(self):
        chosen = input('Pick a player to eliminate')
        chosen.eliminated()


class Spy(Role):
    def __init__(self):
        super().__init__('Spy')

    def night_action(self):
        chosen = input('Choose a player to investigate')
        self.reveal(chosen)

    def reveal(self, target: 'User'):
        return target.role.name
    
class Civilian(Role):
    def __init__(self):
        super().__init__('Civilian')

    def night_action(self):
        print("Zzzzzz")



