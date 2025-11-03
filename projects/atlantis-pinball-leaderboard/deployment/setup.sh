#!/bin/bash

# 🎮 Atlantis Pinball Leaderboard - Setup Script
# Automates the entire setup process

set -e  # Exit on error

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎮  ATLANTIS PINBALL LEADERBOARD SETUP"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed"
    echo "Please install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed"
    echo "Please install Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"
echo ""

# Navigate to project root
cd "$(dirname "$0")/.."
PROJECT_ROOT=$(pwd)

echo "📂 Project root: $PROJECT_ROOT"
echo ""

# Step 1: Check Python for database seeding
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "STEP 1: Database Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if ! command -v python3 &> /dev/null; then
    echo "⚠️  Python 3 not found. Skipping database seeding."
    echo "   You can seed manually later with: cd src/backend && python seed_data.py"
else
    echo "🐍 Installing Python dependencies..."
    cd "$PROJECT_ROOT/src/backend"
    python3 -m pip install -q -r requirements.txt
    
    echo "🌱 Seeding database with whiteboard data..."
    echo "yes" | python3 seed_data.py
    
    echo "✅ Database seeded with 25 players"
fi

echo ""

# Step 2: Build Docker containers
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "STEP 2: Building Docker Containers"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cd "$PROJECT_ROOT/deployment"
echo "🐳 Building containers (this may take a few minutes)..."
docker-compose build

echo "✅ Containers built successfully"
echo ""

# Step 3: Start services
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "STEP 3: Starting Services"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

docker-compose up -d

echo "✅ Services started"
echo ""

# Step 4: Health check
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "STEP 4: Health Check"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "⏳ Waiting for services to be ready..."
sleep 5

# Check backend health
if curl -s http://localhost:8000/api/health > /dev/null; then
    echo "✅ Backend API is healthy"
else
    echo "⚠️  Backend API may not be ready yet"
fi

# Check frontend
if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Frontend is healthy"
else
    echo "⚠️  Frontend may not be ready yet"
fi

echo ""

# Final summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉  SETUP COMPLETE!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🎮 Atlantis Pinball Leaderboard is now running!"
echo ""
echo "📍 Access Points:"
echo "   • Leaderboard Display:  http://localhost:3000"
echo "   • Add Score (Mobile):   http://localhost:3000/add"
echo "   • Admin Panel:          http://localhost:3000/admin"
echo "   • Backend API:          http://localhost:8000"
echo "   • API Docs:             http://localhost:8000/docs"
echo ""
echo "📊 Container Status:"
docker-compose ps
echo ""
echo "💡 Useful Commands:"
echo "   • View logs:       docker-compose logs -f"
echo "   • Stop services:   docker-compose down"
echo "   • Restart:         docker-compose restart"
echo ""
echo "🎮 Semper Fi! Enjoy your Tron-themed leaderboard!"
echo ""

