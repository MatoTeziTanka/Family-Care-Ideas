"""
Data models for Atlantis Pinball Leaderboard
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# =============================================================================
# PLAYER MODELS
# =============================================================================

class PlayerBase(BaseModel):
    """Base player model"""
    name: str = Field(..., min_length=1, max_length=50)


class PlayerCreate(PlayerBase):
    """Model for creating a new player"""
    pass


class Player(PlayerBase):
    """Complete player model"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# =============================================================================
# SCORE MODELS
# =============================================================================

class ScoreBase(BaseModel):
    """Base score model"""
    score: int = Field(..., ge=0, description="Score must be non-negative")
    player_id: int = Field(..., gt=0)


class ScoreCreate(ScoreBase):
    """Model for creating a new score"""
    verified: bool = False
    photo_url: Optional[str] = None


class Score(ScoreBase):
    """Complete score model"""
    id: int
    player_name: str
    created_at: datetime
    verified: bool
    photo_url: Optional[str] = None
    
    class Config:
        from_attributes = True


# =============================================================================
# LEADERBOARD MODELS
# =============================================================================

class LeaderboardEntry(BaseModel):
    """Leaderboard entry with ranking"""
    rank: int
    player_id: int
    name: str
    high_score: int
    games_played: int
    avg_score: int
    last_played: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# =============================================================================
# STATISTICS MODELS
# =============================================================================

class PlayerStats(BaseModel):
    """Detailed player statistics"""
    player: Player
    rank: int
    games_played: int
    high_score: int
    low_score: int
    avg_score: int
    last_played: Optional[datetime] = None
    
    class Config:
        from_attributes = True

