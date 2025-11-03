# 🎮 ATLANTIS PINBALL LEADERBOARD

**Tron-themed digital leaderboard for 1975 Gottlieb Atlantis pinball machine**

![Status](https://img.shields.io/badge/status-active-brightgreen)
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 🎯 Overview

A real-time digital leaderboard system combining the nostalgia of 1975 pinball with 1982 Tron aesthetics and modern 2025 web technology. Built for Seth's Atlantis pinball machine with:

- 🎨 **Tron Aesthetic** - Cyan/orange neon glow, animated grid backgrounds, 8-bit fusion
- 📊 **Real-time Updates** - WebSocket-powered live score display
- 📱 **Multiple Input Methods** - Mobile web, voice commands, SMS, API
- 🖥️ **Vertical Display** - Portrait mode optimized for arcade cabinet style
- 🔐 **Self-hosted** - Runs on Dell R730 server at `pinball.lightspeedup.com`

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for local development)

### 1. Clone Repository

```bash
git clone https://github.com/MatoTeziTanka/Family-Care-Ideas.git
cd Family-Care-Ideas/projects/atlantis-pinball-leaderboard
```

### 2. Seed Database

```bash
cd src/backend
pip install -r requirements.txt
python seed_data.py
```

### 3. Run with Docker

```bash
cd deployment
docker-compose up -d
```

### 4. Access Application

- **Leaderboard Display:** http://localhost
- **Add Score:** http://localhost/add
- **Admin Panel:** http://localhost/admin

---

## 📂 Project Structure

```
atlantis-pinball-leaderboard/
├── src/
│   ├── backend/              # FastAPI backend
│   │   ├── main.py          # API routes
│   │   ├── models.py        # Data models
│   │   ├── database.py      # Database config
│   │   ├── websockets.py    # Real-time updates
│   │   ├── seed_data.py     # Database seeding
│   │   └── requirements.txt
│   └── frontend/            # React frontend
│       ├── src/
│       │   ├── views/       # Page views
│       │   ├── components/  # Reusable components
│       │   └── styles/      # Tron CSS
│       └── package.json
├── deployment/              # Docker & deployment
│   ├── docker-compose.yml
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── nginx.conf
├── docs/                    # Documentation
│   └── DEVELOPMENT-HANDOVER.md
├── assets/                  # Data & images
│   └── WHITEBOARD-DATA.md
└── README.md
```

---

## 🛠️ Development

### Backend (FastAPI)

```bash
cd src/backend
pip install -r requirements.txt

# Seed database
python seed_data.py

# Run development server
python main.py
# or
uvicorn main:app --reload --port 8000
```

API will be available at `http://localhost:8000`

**API Endpoints:**
- `GET /api/health` - Health check
- `GET /api/leaderboard` - Get top players
- `GET /api/leaderboard/recent` - Recent scores
- `GET /api/players` - List all players
- `POST /api/scores` - Add new score
- `DELETE /api/scores/{id}` - Delete score (admin)
- `WS /ws` - WebSocket connection

### Frontend (React + Vite)

```bash
cd src/frontend
npm install

# Run development server
npm run dev
```

Frontend will be available at `http://localhost:3000`

**Views:**
- `/` - Main leaderboard display (vertical)
- `/add` - Mobile score entry form
- `/admin` - Admin management panel

---

## 🎨 Design System

### Color Palette

- **Cyan:** `#00D9FF` - Primary program color
- **Orange:** `#FF9500` - Warning/highlight
- **Deep Black:** `#000000` - Background
- **Dark Blue:** `#0A0E27` - Secondary background
- **Gold:** `#FFD700` - 1st place
- **Silver:** `#C0C0C0` - 2nd place
- **Bronze:** `#CD7F32` - 3rd place

### Typography

- **Primary:** Orbitron (futuristic, geometric)
- **Retro:** Press Start 2P (8-bit style)

### Effects

- Neon glow text shadows
- Pulsing animations for top 3
- Grid background patterns
- Particle effects
- Scanline CRT simulation

---

## 🚢 Deployment

### Docker Deployment (Recommended)

```bash
cd deployment
docker-compose up -d
```

Services:
- **Backend:** Port 8000
- **Frontend:** Port 3000
- **Nginx:** Port 80/443

### Manual Deployment

1. **Backend:**
```bash
cd src/backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

2. **Frontend:**
```bash
cd src/frontend
npm install
npm run build
# Serve dist/ folder with nginx or similar
```

### Production Notes

- Configure SSL certificates in `deployment/nginx.conf`
- Update `CORS_ORIGINS` in backend environment
- Set up automatic backups for SQLite database
- Consider PostgreSQL for production at scale

---

## 📱 Input Methods

### 1. Web Interface

**Add Score:** Navigate to `/add` on mobile or desktop

### 2. Direct API

```bash
curl -X POST http://pinball.lightspeedup.com/api/scores \
  -H "Content-Type: application/json" \
  -d '{
    "player_id": 1,
    "score": 50000
  }'
```

### 3. Voice Commands (Phase 2)

- **Alexa:** "Alexa, tell Atlantis Pinball Seth scored 50,000"
- **Google:** "Hey Google, update Atlantis score for Seth to 50,000"

### 4. SMS (Phase 2)

Text to dedicated number: `Seth 50000`

---

## 📊 Database Schema

```sql
-- Players
CREATE TABLE players (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Scores
CREATE TABLE scores (
    id INTEGER PRIMARY KEY,
    player_id INTEGER REFERENCES players(id),
    score INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verified BOOLEAN DEFAULT FALSE,
    photo_url VARCHAR(255)
);
```

---

## 🎯 Roadmap

### Phase 1: MVP ✅ (COMPLETE)
- [x] Basic leaderboard display
- [x] Web score entry
- [x] Tron aesthetic styling
- [x] Real-time WebSocket updates
- [x] Docker deployment

### Phase 2: Enhanced (In Progress)
- [ ] Alexa skill integration
- [ ] Google Assistant action
- [ ] SMS integration (Twilio)
- [ ] Player statistics page
- [ ] Achievement badges

### Phase 3: Advanced
- [ ] Photo verification
- [ ] Multi-machine support
- [ ] Email notifications
- [ ] Sound effects
- [ ] Mobile PWA

---

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
DATABASE_URL=sqlite:///data/atlantis_pinball.db
API_PORT=8000
CORS_ORIGINS=*
```

### Display Rotation (Raspberry Pi)

For vertical portrait display:

```bash
# Edit /boot/config.txt
display_rotate=1  # 90° clockwise

# Auto-start browser in kiosk mode
# Edit /etc/xdg/lxsession/LXDE-pi/autostart
@chromium-browser --kiosk --app=http://pinball.lightspeedup.com
```

---

## 🐛 Troubleshooting

### WebSocket Connection Issues

- Check firewall allows WebSocket connections
- Verify proxy configuration for `/ws` endpoint
- Ensure backend is running and accessible

### Database Locked

SQLite can lock with concurrent writes. Consider PostgreSQL for production:

```bash
DATABASE_URL=postgresql://user:pass@localhost:5432/atlantis
pip install asyncpg
```

### Display Not Updating

- Check browser console for WebSocket errors
- Verify backend health: `curl http://localhost:8000/api/health`
- Restart Docker containers: `docker-compose restart`

---

## 👤 Author

**Seth Schultz**  
USMC Veteran  
[LightSpeedUp Hosting](https://lightspeedup.com)

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🎮 Semper Fi

*Built with pride for the 1975 Gottlieb Atlantis pinball machine*

**"Build something that looks as cool as it functions."** 🎮💙

---

**Last Updated:** November 3, 2025  
**Version:** 1.0.0

