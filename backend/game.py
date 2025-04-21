import random
import time
import uuid
from abc import ABC, abstractmethod
from collections import defaultdict


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
        self.remaining_players = []
        self.remaining_players_number = len(self.remaining_players)
        self.assigned_roles = defaultdict(list) # regular_dict = dict(self.assigned_roles)
        self.day_timer = Timer(self.settings['day length'])
        self.night_timer = Timer(self.settings['night length'])
    
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

        self.game_state = 'game started'

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

    def day_phase(self):
        # Set voting instance
        self.day_vote = Vote(self, 'lobby')
        self.day_vote.start_voting()

    def night_action_phase(self):
        for user in self.users.values():
            user.role.night_action(self)

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
        self.users[user_id].alive = False
        self.eliminated.append(self.users[user_id].id)
        self.remaining_players.remove(self.users[user_id].id)

    def new_game(self):
        for user in self.users.values(): 
            self.remaining_players.append(user.id)
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


class Vote:
    def __init__(self, lobby: 'Lobby', voters: str):
        self.lobby = lobby
        self.votes = {} # key: user, value: number of votes
        self.user_vote = {} # key: voter_id, value: user_voted 
        self.leading_votes = [] # List of user/s with most votes
        self.voters = voters # Killers or lobby
        if self.voters == 'lobby':
            self.timer = self.lobby.day_timer
        elif self.voters == 'killers':
            self.timer = self.lobby.night_timer

    def start_voting(self):
        # Add all active users with 0 votes
        self.votes = {user_id: 0 for user_id in self.lobby.users.keys() if user_id in self.lobby.remaining_players}
        self.user_vote = {}
        self.timer.start(self)

    def cast_vote(self, voter_id, target_id):
        # Validate target is alive
        if target_id not in self.lobby.remaining_players:
            raise ValueError("Invalid target") # Maybe validate in redis_service.py?
        # Killers can't vote other killers
        if self.voters == 'killers':
            if target_id in self.lobby.killers:
                raise ValueError("Can't kill a killer")
        # Remove previous vote if exists
        if voter_id in self.user_vote:
            prev_target = self.user_vote[voter_id]
            self.votes[prev_target] -= 1

        # Add new vote
        self.user_vote[voter_id] = target_id
        self.votes[target_id] += 1

    # Check for majority based on total active users, for auto-submit
    def check_majority(self):
        if self.voters == 'lobby':
            active_users = len(self.lobby.remaining_players)
            majority_threshold = active_users // 2 # Round down
        elif self.voters == 'killers':
            active_killers = [killer for killer in self.lobby.killers if self.lobby.users[killer].alive]
            majority_threshold = len(active_killers) // 2

        for user_id, count in self.votes.items():
            # Must be greater to avoid 2/4 and still accepts 3/5
            if count > majority_threshold:
                return user_id
        # If no majority has been found, continue with vote
        return None
    
    def get_leading_vote(self):
        if not self.votes:
            return None
        
        highest_vote_count = max(self.votes.values())

        if highest_vote_count == 0:
            return None
        
        self.leading_votes = [user_id for user_id, count in self.votes.items() if count == highest_vote_count]
        if len(self.leading_votes) == 1: 
            return self.leading_votes[0]
        return None # Tie. May change to choose random on tie in future
    

class Timer:
    def __init__(self, duration: int):
        self.active = False
        self.duration = duration
        self.start_time = 0
        self.vote = None

    def _get_remaining_time(self) -> int:
        if not self.active:
            return 0
        elapsed = time.time() - self.start_time
        remaining = round(self.duration - elapsed)
        return int(remaining)
    
    def _run_timer(self):
        while self.active and self._get_remaining_time() > 0:
            if self.vote:
                # Check for max votes to end timer early
                voted = self.vote.check_majority()
                if voted:
                    # End Voting period if lobby
                    if self.vote.voters == 'lobby':
                        self.active = False
                        return voted
            # Add functionality to check if all night actions are completed to end timer early
            time.sleep(0.1)
        
        # Time completed
        if self.active:
            self.active = False
            return self.vote.get_leading_vote()
        
    def start(self, vote: Vote = None):
        if vote:
            self.vote = vote
        self.active = True
        self.start_time = time.time()
        self._run_timer()


class Role(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def night_action(self, lobby: 'Lobby'):
        pass

    @abstractmethod
    def perform_night_action(self):
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
        active_players = lobby.remaining_players
        # vote for kill
        voting = Vote(lobby, 'killers')
        voting.start_voting()
        # send list of active ids, to verify valid vote

    def perform_night_action(self, target_id: 'User.id', lobby: 'Lobby'):
        lobby.eliminate(target_id)


class Spy(Role):
    def __init__(self):
        super().__init__('Spy')

    def night_action(self, lobby: 'Lobby'):
        chosen: 'User' = input('Choose a player to investigate')
        self.reveal(chosen)

    def reveal(self, target: 'User'):
        return target.role.name
    
class Civilian(Role):
    def __init__(self):
        super().__init__('Civilian')

    def night_action(self, lobby: 'Lobby'):
        # send action to sleep
        pass

    def perform_night_action(self):
        return super().perform_night_action()



