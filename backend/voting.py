from typing import Optional
import asyncio

def setup_vote(usernames: list) -> tuple[dict, dict]:
    # Set votes to zero for active players (using usernames)
    votes = {username: 0 for username in usernames} # key: username, value: no. of votes
    user_vote = {} # key: voter_id, value: target_username

    return votes, user_vote

def check_majority(voters: int, votes: dict) -> Optional[str]:
    """Returns username with majority if found, None otherwise"""
    threshold = voters // 2
    for username, count in votes.items():
        if count > threshold:
            return username
    return None

def all_voted(remaining: int, user_votes: int) -> bool:
    return user_votes == remaining

def get_leading_vote(votes: dict) -> Optional[str]:
    """Returns username with most votes, None if tie or no votes"""
    if not votes:
        return None
    
    highest_vote_count = max(votes.values())

    if highest_vote_count == 0:
        return None
    
    leading_vote = [username for username, count in votes.items() if count == highest_vote_count]
    if len(leading_vote) == 1:
        return leading_vote[0]
    return None # Ties return none

async def timer(duration):
    try:
        await asyncio.sleep(duration)
    except asyncio.CancelledError:
        pass
    