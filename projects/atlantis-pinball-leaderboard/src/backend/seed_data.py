"""
Seed database with whiteboard data
25 players with their high scores
"""
import asyncio
import databases
from database import DATABASE_URL, init_db, get_db

# Whiteboard data (from WHITEBOARD-DATA.md)
WHITEBOARD_DATA = [
    {"name": "Jason", "score": 77750},
    {"name": "Kenley", "score": 76590},
    {"name": "Elyse", "score": 75340},
    {"name": "Dustin", "score": 72390},
    {"name": "Ted", "score": 66260},
    {"name": "Seth", "score": 66240},
    {"name": "Mike", "score": 61450},
    {"name": "Kenny", "score": 59710},
    {"name": "Nicole", "score": 52350},
    {"name": "Dan", "score": 52150},
    {"name": "Dawn", "score": 47930},
    {"name": "Tyler", "score": 47210},
    {"name": "Scott", "score": 46790},
    {"name": "Eden", "score": 45360},
    {"name": "William", "score": 42570},
    {"name": "Hank", "score": 42350},
    {"name": "Z-Ha", "score": 42090},
    {"name": "Darwin", "score": 41370},
    {"name": "Ralph", "score": 39440},
    {"name": "Jackson", "score": 36760},
    {"name": "Sessic", "score": 35570},
    {"name": "mom Clark", "score": 35100},
    {"name": "Millie", "score": 32660},
    {"name": "Ash", "score": 25520},
    {"name": "Elsa", "score": 25100},
]


async def seed_database():
    """Seed database with whiteboard data"""
    print("🎮 Seeding Atlantis Pinball Leaderboard...")
    
    # Initialize database
    await init_db()
    db = await get_db()
    
    # Check if data already exists
    existing_players = await db.fetch_all("SELECT * FROM players")
    if existing_players:
        print(f"⚠️  Database already has {len(existing_players)} players")
        response = input("Clear and reseed? (yes/no): ")
        if response.lower() != "yes":
            print("❌ Seeding cancelled")
            return
        
        # Clear existing data
        await db.execute("DELETE FROM scores")
        await db.execute("DELETE FROM players")
        print("🗑️  Cleared existing data")
    
    # Insert players and scores
    for idx, player_data in enumerate(WHITEBOARD_DATA, 1):
        # Insert player
        player_id = await db.execute(
            "INSERT INTO players (name) VALUES (?)",
            [player_data["name"]]
        )
        
        # Insert their high score
        await db.execute(
            "INSERT INTO scores (player_id, score, verified) VALUES (?, ?, ?)",
            [player_id, player_data["score"], True]
        )
        
        print(f"✅ {idx}/25 - {player_data['name']}: {player_data['score']:,}")
    
    print("\n🎮 Database seeded successfully!")
    print(f"📊 Total players: {len(WHITEBOARD_DATA)}")
    print(f"🏆 High score: {max(p['score'] for p in WHITEBOARD_DATA):,} (Jason)")
    print(f"📍 Database location: {DATABASE_URL}")
    
    await db.disconnect()


if __name__ == "__main__":
    asyncio.run(seed_database())

