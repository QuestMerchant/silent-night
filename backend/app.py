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

class CreateLobbyResponse(BaseModel):
    username: str
    lobbyCode: str
    userId: str

class JoinLobbyRequest(BaseModel):
    avatar: str
    lobbyCode: str
    userId: Optional[str] = None

class JoinLobbyResponse(BaseModel):
    userId: str
    username: str

class StartGameRequest(BaseModel):
    lobbyCode: str

# Helper function to generate random username
def generateUsername() -> str:
    adjectives = ['Swift', 'Silent', 'Shadow', 'Mystic', 'Brave', 'Clever', 'Fierce', 'Noble', 'Wise', 'Bold']
    nouns = ['Wolf', 'Raven', 'Fox', 'Eagle', 'Tiger', 'Lion', 'Bear', 'Hawk', 'Falcon', 'Panther']
    number = random.randint(100, 999)
    return f"{random.choice(adjectives)}{random.choice(nouns)}{number}"

# Serve frontend (optional)
@app.get("/")
async def serve_frontend():
    frontend_path = '../frontend/dist/index.html'
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    return {"message": "Frontend not built"}

@app.get("/{path:path}")
async def serve_static(path: str):
    static_path = f'../frontend/dist/{path}'
    if os.path.exists(static_path):
        return FileResponse(static_path)
    raise HTTPException(status_code=404, detail="File not found")

@app.post("/create_lobby", response_model=CreateLobbyResponse)
async def createLobby(request: CreateLobbyRequest):
    try:
        # Generate random username
        username = generateUsername()
        
        # Create lobby in Redis
        lobby = gameService.create_lobby(username, request.avatar)
        
        return CreateLobbyResponse(
            username=username,
            lobbyCode=lobby['lobby_code'],
            userId=lobby['host_id']
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/join_lobby", response_model=JoinLobbyResponse)
async def joinLobby(request: JoinLobbyRequest):
    try:
        # Generate random username
        username = generateUsername()
        
        # Join lobby in Redis
        result = gameService.join_lobby(
            request.lobbyCode,
            username,
            request.avatar,
            request.userId
        )
        
        # Send Pusher event
        pusherClient.trigger(
            f'lobby-{request.lobbyCode}',
            'user_joined',
            {'name': username}
        )
        
        return JoinLobbyResponse(
            userId=result['user_id'],
            username=username
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/start_game")
async def startGame(
    request: StartGameRequest,
    user_id: Optional[str] = Header(None, alias="user-id")
):
    if not user_id:
        raise HTTPException(status_code=401, detail="user-id header required")
    
    try:
        # Verify user is host (you'll add this check in game_start method later)
        gameService.game_start(request.lobbyCode)
        
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
