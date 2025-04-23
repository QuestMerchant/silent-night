from typing import Optional
import asyncio

def setup_vote(users: list) -> tuple[dict, dict, list]:
    # Set votes to zero for active players
    votes = {user_id: 0 for user_id in users} # key: user, value: no. of votes
    user_vote = {} # key: voter, value: user voted
    leading_votes = []

    return votes, user_vote, leading_votes

def check_majority(voters: int, votes: dict) -> Optional[bool]:
    threshold = voters // 2
    for count in votes.values():
        if count > threshold:
            return True
    return False

def all_voted(remaining: int, user_votes: int) -> bool:
    return user_votes == remaining

def get_leading_vote(votes: dict) -> Optional[str]:
    if not votes:
        return None
    
    highest_vote_count = max(votes.values())

    if highest_vote_count == 0:
        return None
    
    leading_vote = [user_id for user_id, count in votes.items() if count == highest_vote_count]
    if len(leading_vote) == 1:
        return leading_vote[0]
    return None # Ties return none

async def timer(duration):
    try:
        await asyncio.sleep(duration)
    except asyncio.CancelledError:
        pass
    