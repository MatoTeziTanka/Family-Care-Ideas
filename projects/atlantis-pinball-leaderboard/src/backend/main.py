"""
🎮 ATLANTIS PINBALL LEADERBOARD - FASTAPI BACKEND
Tron aesthetic meets 1975 pinball machine
"""
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from typing import List, Optional
import uvicorn
from datetime import datetime
import json

from database import init_db, get_db
from models import (
    Player, Score, ScoreCreate, PlayerCreate, 
    LeaderboardEntry, PlayerStats
)
from websockets import ConnectionManager
from email_notifications import get_notifier

# WebSocket manager for real-time updates
manager = ConnectionManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup"""
    await init_db()
    yield

app = FastAPI(
    title="Atlantis Pinball Leaderboard",
    description="🎮 Tron-themed digital leaderboard for 1975 Gottlieb Atlantis pinball",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# HEALTH CHECK
# =============================================================================

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Atlantis Pinball Leaderboard",
        "timestamp": datetime.utcnow().isoformat()
    }

# =============================================================================
# LEADERBOARD ENDPOINTS
# =============================================================================

@app.get("/api/leaderboard", response_model=List[LeaderboardEntry])
async def get_leaderboard(limit: int = 25):
    """
    Get top players by high score
    Returns ranked list with player stats
    """
    db = await get_db()
    
    query = """
        SELECT 
            RANK() OVER (ORDER BY max_score DESC) as rank,
            p.id,
            p.name,
            MAX(s.score) as high_score,
            COUNT(s.id) as games_played,
            CAST(AVG(s.score) as INTEGER) as avg_score,
            MAX(s.created_at) as last_played
        FROM players p
        LEFT JOIN scores s ON p.id = s.player_id
        GROUP BY p.id, p.name
        ORDER BY high_score DESC
        LIMIT ?
    """
    
    rows = await db.fetch_all(query, [limit])
    
    leaderboard = []
    for row in rows:
        leaderboard.append(LeaderboardEntry(
            rank=row['rank'],
            player_id=row['id'],
            name=row['name'],
            high_score=row['high_score'] or 0,
            games_played=row['games_played'] or 0,
            avg_score=row['avg_score'] or 0,
            last_played=row['last_played']
        ))
    
    return leaderboard

@app.get("/api/leaderboard/recent", response_model=List[Score])
async def get_recent_scores(limit: int = 10):
    """Get most recent score submissions"""
    db = await get_db()
    
    query = """
        SELECT s.*, p.name as player_name
        FROM scores s
        JOIN players p ON s.player_id = p.id
        ORDER BY s.created_at DESC
        LIMIT ?
    """
    
    rows = await db.fetch_all(query, [limit])
    
    scores = []
    for row in rows:
        scores.append(Score(
            id=row['id'],
            player_id=row['player_id'],
            player_name=row['player_name'],
            score=row['score'],
            created_at=row['created_at'],
            verified=row['verified'],
            photo_url=row['photo_url']
        ))
    
    return scores

# =============================================================================
# PLAYER ENDPOINTS
# =============================================================================

@app.get("/api/players", response_model=List[Player])
async def get_players():
    """Get all players"""
    db = await get_db()
    rows = await db.fetch_all("SELECT * FROM players ORDER BY name")
    return [Player(**dict(row)) for row in rows]

@app.get("/api/players/{player_id}", response_model=PlayerStats)
async def get_player_stats(player_id: int):
    """Get detailed stats for a specific player"""
    db = await get_db()
    
    # Get player info
    player_row = await db.fetch_one(
        "SELECT * FROM players WHERE id = ?", [player_id]
    )
    if not player_row:
        raise HTTPException(status_code=404, detail="Player not found")
    
    # Get stats
    stats_query = """
        SELECT 
            COUNT(*) as games_played,
            MAX(score) as high_score,
            MIN(score) as low_score,
            CAST(AVG(score) as INTEGER) as avg_score,
            MAX(created_at) as last_played
        FROM scores
        WHERE player_id = ?
    """
    stats_row = await db.fetch_one(stats_query, [player_id])
    
    # Get rank
    rank_query = """
        SELECT COUNT(*) + 1 as rank
        FROM (
            SELECT MAX(score) as max_score
            FROM scores
            GROUP BY player_id
            HAVING max_score > (
                SELECT MAX(score) FROM scores WHERE player_id = ?
            )
        )
    """
    rank_row = await db.fetch_one(rank_query, [player_id])
    
    return PlayerStats(
        player=Player(**dict(player_row)),
        rank=rank_row['rank'] if rank_row else 1,
        games_played=stats_row['games_played'] or 0,
        high_score=stats_row['high_score'] or 0,
        low_score=stats_row['low_score'] or 0,
        avg_score=stats_row['avg_score'] or 0,
        last_played=stats_row['last_played']
    )

@app.post("/api/players", response_model=Player)
async def create_player(player: PlayerCreate):
    """Create a new player"""
    db = await get_db()
    
    # Check if player already exists
    existing = await db.fetch_one(
        "SELECT * FROM players WHERE name = ?", [player.name]
    )
    if existing:
        raise HTTPException(status_code=400, detail="Player already exists")
    
    # Insert player
    query = "INSERT INTO players (name) VALUES (?)"
    player_id = await db.execute(query, [player.name])
    
    # Get created player
    new_player = await db.fetch_one(
        "SELECT * FROM players WHERE id = ?", [player_id]
    )
    
    return Player(**dict(new_player))

# =============================================================================
# SCORE ENDPOINTS
# =============================================================================

@app.post("/api/scores", response_model=Score)
async def add_score(score_data: ScoreCreate):
    """
    Add a new score
    Broadcasts update via WebSocket to all connected displays
    Sends email notification
    """
    db = await get_db()
    
    # Verify player exists
    player = await db.fetch_one(
        "SELECT * FROM players WHERE id = ?", [score_data.player_id]
    )
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    # Check if this is a high score
    previous_high = await db.fetch_one(
        "SELECT MAX(score) as high_score FROM scores WHERE player_id = ?",
        [score_data.player_id]
    )
    is_high_score = (not previous_high['high_score']) or (score_data.score > previous_high['high_score'])
    
    # Insert score
    query = """
        INSERT INTO scores (player_id, score, verified, photo_url)
        VALUES (?, ?, ?, ?)
    """
    score_id = await db.execute(
        query, 
        [score_data.player_id, score_data.score, 
         score_data.verified, score_data.photo_url]
    )
    
    # Get created score with player name
    score_query = """
        SELECT s.*, p.name as player_name
        FROM scores s
        JOIN players p ON s.player_id = p.id
        WHERE s.id = ?
    """
    new_score = await db.fetch_one(score_query, [score_id])
    
    score = Score(**dict(new_score))
    
    # Get current rank
    rank_query = """
        SELECT COUNT(*) + 1 as rank
        FROM (
            SELECT MAX(score) as max_score
            FROM scores
            GROUP BY player_id
            HAVING max_score > ?
        )
    """
    rank_result = await db.fetch_one(rank_query, [score.score])
    current_rank = rank_result['rank'] if rank_result else 1
    
    # Send email notification
    notifier = get_notifier()
    notifier.send_score_notification(
        player_name=score.player_name,
        score=score.score,
        is_high_score=is_high_score,
        rank=current_rank
    )
    
    # Broadcast to all WebSocket connections
    await manager.broadcast({
        "type": "new_score",
        "data": {
            "id": score.id,
            "player_name": score.player_name,
            "score": score.score,
            "created_at": score.created_at.isoformat()
        }
    })
    
    return score

@app.get("/api/scores/{score_id}", response_model=Score)
async def get_score(score_id: int):
    """Get specific score by ID"""
    db = await get_db()
    
    query = """
        SELECT s.*, p.name as player_name
        FROM scores s
        JOIN players p ON s.player_id = p.id
        WHERE s.id = ?
    """
    row = await db.fetch_one(query, [score_id])
    
    if not row:
        raise HTTPException(status_code=404, detail="Score not found")
    
    return Score(**dict(row))

@app.delete("/api/scores/{score_id}")
async def delete_score(score_id: int):
    """Delete a score (admin only)"""
    db = await get_db()
    
    result = await db.execute("DELETE FROM scores WHERE id = ?", [score_id])
    
    if result == 0:
        raise HTTPException(status_code=404, detail="Score not found")
    
    # Broadcast update
    await manager.broadcast({
        "type": "score_deleted",
        "data": {"score_id": score_id}
    })
    
    return {"message": "Score deleted", "id": score_id}

# =============================================================================
# WEBSOCKET ENDPOINT
# =============================================================================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time updates
    Sends leaderboard changes to all connected displays
    """
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and listen for messages
            data = await websocket.receive_text()
            # Echo for debugging
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# =============================================================================
# SERVE FRONTEND (Production)
# =============================================================================

# Mount static files (React build)
# app.mount("/static", StaticFiles(directory="../frontend/build/static"), name="static")

# @app.get("/")
# async def serve_frontend():
#     return FileResponse("../frontend/build/index.html")

# =============================================================================
# DEVELOPMENT SERVER
# =============================================================================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

