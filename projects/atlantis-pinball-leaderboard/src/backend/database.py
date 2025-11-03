"""
Database configuration and initialization
Uses SQLite for simplicity (can migrate to PostgreSQL later)
"""
import databases
import sqlalchemy
from sqlalchemy import create_engine
import os
from pathlib import Path

# Database file location
DB_DIR = Path(__file__).parent.parent.parent / "data"
DB_DIR.mkdir(exist_ok=True)
DATABASE_URL = f"sqlite:///{DB_DIR}/atlantis_pinball.db"

# Database instance
database = databases.Database(DATABASE_URL)

# SQLAlchemy metadata
metadata = sqlalchemy.MetaData()

# =============================================================================
# TABLES
# =============================================================================

players = sqlalchemy.Table(
    "players",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(50), unique=True, nullable=False),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, 
                     server_default=sqlalchemy.func.now())
)

scores = sqlalchemy.Table(
    "scores",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("player_id", sqlalchemy.Integer, 
                     sqlalchemy.ForeignKey("players.id"), nullable=False),
    sqlalchemy.Column("score", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, 
                     server_default=sqlalchemy.func.now()),
    sqlalchemy.Column("verified", sqlalchemy.Boolean, default=False),
    sqlalchemy.Column("photo_url", sqlalchemy.String(255), nullable=True)
)

# =============================================================================
# DATABASE INITIALIZATION
# =============================================================================

async def init_db():
    """Initialize database and create tables"""
    # Create engine
    engine = create_engine(
        DATABASE_URL.replace("sqlite:///", "sqlite+pysqlite:///"),
        connect_args={"check_same_thread": False}
    )
    
    # Create tables
    metadata.create_all(engine)
    
    # Connect database
    await database.connect()
    
    print(f"✅ Database initialized at {DATABASE_URL}")


async def get_db():
    """Get database connection"""
    return database


async def close_db():
    """Close database connection"""
    await database.disconnect()

