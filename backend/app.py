from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import pusher
import os
import random
from redis_service import GameService

app = FastAPI()

# Initialize Pusher (you'll need to set these as environment variables)
pusherClient = pusher.Pusher(
    app_id=os.getenv('PUSHER_APP_ID', ''),
    key=os.getenv('PUSHER_KEY', ''),
    secret=os.getenv('PUSHER_SECRET', ''),
    cluster=os.getenv('PUSHER_CLUSTER', 'eu'),
    ssl=True
)

# Initialize Redis
gameService = GameService()

# Pydantic models
class CreateLobbyRequest(BaseModel):
    avatar: str
    username: str

class CreateLobbyResponse(BaseModel):
    hostName: str
    lobbyCode: str
    hostId: str

class JoinLobbyRequest(BaseModel):
    avatar: str
    lobbyCode: str
    username: str
    userId: Optional[str] = None

class JoinLobbyResponse(BaseModel):
    userId: str

class StartGameRequest(BaseModel):
    lobbyCode: str

class NightActionRequest(BaseModel):
    lobbyCode: str
    targetUsername: Optional[str] = None  # Required for some roles (Spy, Serial Killer), not needed for others (Civilian)

class CastVoteRequest(BaseModel):
    lobbyCode: str
    targetUsername: str  # Username of the player being voted for

@app.post("/create_lobby", response_model=CreateLobbyResponse)
async def createLobby(request: CreateLobbyRequest):
    try:        
        # Create lobby in Redis
        lobby = gameService.create_lobby(request.username, request.avatar)
        
        return CreateLobbyResponse(
            hostName=request.username,
            lobbyCode=lobby['lobby_code'],
            hostId=lobby['host_id']
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/join_lobby", response_model=JoinLobbyResponse)
async def joinLobby(request: JoinLobbyRequest):
    try:
        # Join lobby in Redis
        result = gameService.join_lobby(
            request.lobbyCode,
            request.username,
            request.avatar,
            request.userId
        )
        
        # Send Pusher event
        pusherClient.trigger(
            f'lobby-{request.lobbyCode}',
            'system',
            {'message': f'{request.username} has joined the lobby'}
        )
        
        return JoinLobbyResponse(
            userId=result['user_id']
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/start_game")
async def startGame(
    request: StartGameRequest,
    user_id: Optional[str] = Header(None, alias="user-id")
):
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized Access")
    
    try:
        # Verify user is host (you'll add this check in game_start method later)
        gameService.game_start(request.lobbyCode, user_id)
        
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/night_action")
async def nightAction(
    request: NightActionRequest,
    user_id: Optional[str] = Header(None, alias="user-id")
):
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized Access")
    
    try:
        result = gameService.perform_night_action(
            request.lobbyCode,
            user_id,
            request.targetUsername
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/cast_vote")
async def castVote(
    request: CastVoteRequest,
    user_id: Optional[str] = Header(None, alias="user-id")
):
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized Access")
    
    try:
        result = gameService.cast_vote(
            request.lobbyCode,
            user_id,
            request.targetUsername
        )
        
        # Broadcast vote update to all players in lobby via Pusher
        pusherClient.trigger(
            f'lobby-{request.lobbyCode}',
            'vote_update',
            {
                'votes': result['votes'],
                'user_votes': result['user_votes'],
                'is_complete': result['is_complete'],
                'eliminated_username': result['eliminated_username']
            }
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
