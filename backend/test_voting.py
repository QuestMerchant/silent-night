import pytest
from voting import setup_vote, check_majority, all_voted, get_leading_vote

def test_setup():
    users = ['user1','user2','user3']
    votes, user_vote, leading_vote = setup_vote(users) 

    # Check data types
    assert isinstance(votes, dict)
    assert isinstance(user_vote, dict)
    assert isinstance(leading_vote, list)

    # Check that each vote has user id with 0 votes
    for user in users:
        assert user in votes
        assert votes[user] == 0

    # Check that user and leading vote is empty
    assert user_vote == {}
    assert leading_vote == []

def test_majority():
    votes1 = {'user1':0, 'user2':5}
    votes2 = {'user1':0, 'user2':2}

    # below threshold (6)
    assert check_majority(12, votes1) == False
    # above threshold(4)
    assert check_majority(9, votes1) == True
    # equal to threshold (2)
    assert check_majority(4, votes2) == False
    assert check_majority(3, votes2) == True

def test_all():
    assert all_voted(3,3) == True
    assert all_voted(7,6) == False