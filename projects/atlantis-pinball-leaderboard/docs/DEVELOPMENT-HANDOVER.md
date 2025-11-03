# 🎮 ATLANTIS PINBALL LEADERBOARD - DEVELOPMENT HANDOVER

**Project Name:** Atlantis Pinball Leaderboard  
**Date Created:** November 3, 2025  
**Project Owner:** Seth Schultz  
**Purpose:** Digital high score leaderboard for 1975 Gottlieb Atlantis pinball machine  
**Aesthetic:** Tron (1982) + Tron: Legacy (2010) + Tron 2025/2026 - with 8-bit fusion  
**Repository:** (To be created)

---

## 📋 **TABLE OF CONTENTS**

1. [Project Vision](#project-vision)
2. [Current Setup & Data](#current-setup--data)
3. [Technical Requirements](#technical-requirements)
4. [Design Aesthetic](#design-aesthetic)
5. [Architecture Options](#architecture-options)
6. [Input Methods](#input-methods)
7. [Display Options](#display-options)
8. [LightSpeedUp Integration](#lightspeedup-integration)
9. [File Structure](#file-structure)
10. [Deployment Strategy](#deployment-strategy)
11. [Next Steps](#next-steps)

---

## 🎯 **PROJECT VISION**

### **The Problem**
Seth and his friends have been tracking high scores on a **dry erase whiteboard** for their 1975 D. Gottlieb & Co. **Atlantis pinball machine**. It works, but:
- Scores get accidentally erased
- No history tracking
- Manual updates only
- Not shareable remotely
- Not very cool looking

### **The Solution**
A **digital leaderboard system** that:
- ✅ Displays scores on vertical monitor (arcade cabinet style)
- ✅ Tron aesthetic (1980s + 2025/2026 fusion with 8-bit elements)
- ✅ Multiple input methods (phone, web, voice, manual entry)
- ✅ Self-hosted on Seth's Dell server
- ✅ Accessible remotely by friends
- ✅ Castable to TV or direct HDMI display
- ✅ Real-time updates
- ✅ Score history and statistics

### **Why This Is Awesome**
- **Nostalgia:** 1975 pinball machine meets 1982 Tron meets 2025 tech
- **Friends:** Everyone can update scores remotely
- **Epic Display:** Vertical format like classic arcades
- **Bragging Rights:** Permanent digital record
- **Extendable:** Can add more machines later

---

## 📊 **CURRENT SETUP & DATA**

### **The Machine**
- **Name:** Atlantis
- **Manufacturer:** D. Gottlieb & Co.
- **Year:** 1975
- **Players:** 2-4 players
- **Theme:** Underwater/Atlantis city
- **Type:** Electro-mechanical (EM) pinball

### **Current Players & Scores**
**25 players tracked** (extracted from whiteboard photos):

**Top 10:**
1. **Jason** - 77,750 🏆
2. **Kenley** - 76,590 🥇
3. **Elyse** - 75,340 🥈
4. **Dustin** - 72,390 🥉
5. **Ted** - 66,260
6. **Seth** - 66,240
7. **Mike** - 61,450
8. **Kenny** - 59,710
9. **Nicole** - 52,350
10. **Dan** - 52,150

*Full leaderboard data: [`assets/WHITEBOARD-DATA.md`](../assets/WHITEBOARD-DATA.md)*

### **Score Statistics**
- **Highest:** 77,750 (Jason)
- **Lowest:** 25,100 (Elsa)
- **Average:** ~48,828
- **Range:** 52,650 points

---

## 🔧 **TECHNICAL REQUIREMENTS**

### **Must Have**

#### **1. Display Requirements**
- **Orientation:** Vertical (portrait mode) - 90° rotated
- **Resolution:** 1080x1920 (1920x1080 rotated) or higher
- **Refresh:** Real-time updates (websockets)
- **Format:** Full-screen kiosk mode

#### **2. Input Methods** (Multiple Ways to Update Scores)
- 📱 **Mobile Web App** - Touch-friendly score entry
- 💻 **Desktop Web Interface** - Admin panel
- 🗣️ **Voice Commands:**
  - Amazon Alexa: "Alexa, tell Atlantis Pinball Seth scored 50,000"
  - Google Assistant: "Hey Google, update Atlantis score for Seth to 50,000"
- 📲 **SMS/Text** - Text score to a number
- 🔗 **API** - Direct POST requests
- ⌨️ **Manual Entry** - Quick admin form

#### **3. Data Management**
- **Database:** SQLite (simple) or PostgreSQL (robust)
- **Backup:** Daily automatic backups
- **History:** Track all scores, not just high scores
- **Statistics:** Games played, average scores, trends

#### **4. Access Control**
- **Public View:** Anyone can see leaderboard
- **Authenticated Updates:** Only registered players can add scores
- **Admin Panel:** Seth can edit/delete/manage

#### **5. Hosting**
- Self-hosted on Dell R730 server
- Accessible via web browser
- Castable to monitor/TV
- Raspberry Pi option for dedicated display

### **Nice to Have**
- 🏆 Achievement badges
- 📊 Player statistics pages
- 📸 Score verification (photo upload)
- 🎮 Multiple machine support (future)
- 📧 Email notifications (new high score)
- 🎵 Sound effects (arcade sounds)
- 📱 Mobile app (PWA)
- 🎥 Webcam integration (score photo)

---

## 🎨 **DESIGN AESTHETIC**

### **Tron Fusion Concept**

**Blend THREE eras:**

#### **1. Tron (1982) - Classic Elements**
- Cyan and orange neon glow
- Black backgrounds
- Grid patterns (isometric)
- Vector graphics feel
- Geometric shapes
- Light cycles aesthetic

#### **2. 8-Bit Arcade (1975-1985)**
- Pixel fonts (but high-res)
- Retro color palettes
- Scanline effects (subtle)
- CRT glow simulation
- Arcade cabinet vibes

#### **3. Tron 2025/2026 - Modern Polish**
- Smooth animations (CSS3, WebGL)
- Glass morphism elements
- Particle effects
- Dynamic lighting
- 4K ready
- Responsive design

### **Color Palette**

**Primary Colors:**
- **Cyan:** `#00D9FF` (Tron program color)
- **Orange:** `#FF9500` (Tron warning/highlight)
- **Deep Black:** `#000000` (background)
- **Dark Blue:** `#0A0E27` (secondary background)

**Accent Colors:**
- **White:** `#FFFFFF` (text, highlights)
- **Yellow:** `#FFD700` (#1 gold)
- **Silver:** `#C0C0C0` (#2 silver)
- **Bronze:** `#CD7F32` (#3 bronze)
- **Purple:** `#9D00FF` (special effects)

**Neon Glow:**
```css
text-shadow: 
  0 0 5px #00D9FF,
  0 0 10px #00D9FF,
  0 0 20px #00D9FF,
  0 0 40px #00D9FF;

box-shadow:
  0 0 10px #00D9FF,
  0 0 20px #00D9FF,
  0 0 30px #00D9FF,
  inset 0 0 10px #00D9FF;
```

### **Typography**

**Primary Font (8-bit meets modern):**
- **Option 1:** Press Start 2P (Google Fonts) - Pure 8-bit
- **Option 2:** Orbitron (Google Fonts) - Futuristic, geometric
- **Option 3:** Audiowide (Google Fonts) - Retro-futuristic
- **Option 4:** Custom pixel font with anti-aliasing

**Scores:** Large, bold, glowing numbers  
**Names:** Medium, uppercase, tracked spacing  
**Rank:** Extra large, neon outline

### **Layout (Vertical Format)**

```
┌─────────────────────────┐
│     ATLANTIS            │ ← Header (Tron logo style)
│    PINBALL              │
│   HIGH SCORES           │
├─────────────────────────┤
│                         │
│  🥇 #1                  │ ← Gold crown
│  KENLEY                 │    Animated glow
│  76,590                 │    Largest font
│                         │
│  🥈 #2                  │ ← Silver
│  JASON                  │    Medium glow
│  77,750                 │
│                         │
│  🥉 #3                  │ ← Bronze
│  ELYSE                  │    Subtle glow
│  75,340                 │
│                         │
│  #4  DUSTIN    72,390   │ ← Standard entries
│  #5  TED       66,260   │    Scrolling
│  #6  SETH      66,240   │    if needed
│  ...                    │
│                         │
├─────────────────────────┤
│  LATEST GAME:           │ ← Recent activity
│  SETH - 45,000          │    Ticker at bottom
│  2 minutes ago          │
└─────────────────────────┘
```

### **Animation Effects**

**Entry Animations:**
- New high score: Explode onto screen with particles
- Score update: Flash and glow pulse
- Rank change: Slide animation with trail effect

**Idle Animations:**
- Gentle pulsing glow on top 3
- Scrolling grid background
- Particle field (slow moving dots)
- Occasional light beam sweep

**Sound Effects (Optional):**
- New high score: Tron "recognizer" sound
- Score entry: Classic pinball "ding"
- Rank change: Whoosh sound

---

## 🏗️ **ARCHITECTURE OPTIONS**

### **Option 1: React + FastAPI (RECOMMENDED)**

**Why:** Modern, fast, flexible, great for real-time updates

**Frontend:**
- **React** - Component-based UI
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Smooth animations
- **Socket.IO Client** - Real-time updates

**Backend:**
- **FastAPI** (Python) - Fast, modern API
- **SQLite/PostgreSQL** - Database
- **Socket.IO** - Websockets for real-time
- **Uvicorn** - ASGI server

**Real-time Updates:**
```
User adds score → FastAPI → Database → WebSocket → All connected displays update instantly
```

**Tech Stack:**
```
React (Frontend)
    ↓
FastAPI (Backend API)
    ↓
PostgreSQL (Database)
    ↓
Redis (Caching)
    ↓
Docker (Deployment)
```

---

### **Option 2: Next.js Full-Stack**

**Why:** Simpler deployment, built-in API routes

**Tech Stack:**
- **Next.js** - React + API routes
- **Prisma** - Database ORM
- **PostgreSQL** - Database
- **Tailwind** - Styling
- **Vercel/Docker** - Deployment

**Pros:**
- Single codebase
- Built-in API
- Server-side rendering

**Cons:**
- Heavier than FastAPI
- Less flexible for voice integration

---

### **Option 3: Vanilla JS + Node.js**

**Why:** Lightweight, simple, fast

**Tech Stack:**
- **HTML/CSS/JS** - Pure frontend
- **Node.js + Express** - Backend
- **SQLite** - Database
- **Socket.IO** - Websockets

**Pros:**
- Lightweight
- Fast
- Easy to understand

**Cons:**
- More manual work
- Less structure

---

## 📱 **INPUT METHODS**

### **1. Mobile Web App**

**Features:**
- Touch-optimized score entry
- Player name autocomplete
- Quick score buttons (10k, 20k, 30k, etc.)
- Photo upload (optional)
- Offline support (PWA)

**UI:**
```
┌─────────────────────┐
│  ADD NEW SCORE      │
├─────────────────────┤
│  Player: [Seth ▼]   │ ← Dropdown
│  Score:  [_______]  │ ← Number input
│                     │
│  Quick Add:         │
│  [10k] [20k] [30k]  │ ← Buttons
│  [40k] [50k] [60k]  │
│                     │
│  [SUBMIT SCORE]     │ ← Big button
└─────────────────────┘
```

**URL:** `https://pinball.lightspeedup.com/add`

---

### **2. Voice Commands**

#### **Amazon Alexa Skill**

**Skill Name:** "Atlantis Pinball"

**Invocations:**
- "Alexa, tell Atlantis Pinball Seth scored 50,000"
- "Alexa, ask Atlantis Pinball for the high score"
- "Alexa, ask Atlantis Pinball who's winning"

**Setup:**
1. Create Alexa Skill in Amazon Developer Console
2. Configure intents:
   - `AddScoreIntent` - Add new score
   - `GetHighScoreIntent` - Get top score
   - `GetLeaderboardIntent` - Get top 5

3. Create Lambda function (or webhook to FastAPI)
4. Handle requests and update database

**Sample Code:**
```python
# FastAPI endpoint for Alexa
@app.post("/api/alexa")
async def alexa_webhook(request: Request):
    data = await request.json()
    intent = data['request']['intent']['name']
    
    if intent == 'AddScoreIntent':
        player = data['request']['intent']['slots']['player']['value']
        score = data['request']['intent']['slots']['score']['value']
        # Add to database
        return alexa_response(f"{player} scored {score}!")
```

---

#### **Google Assistant Action**

**Action Name:** "Atlantis Pinball Scores"

**Invocations:**
- "Hey Google, tell Atlantis Pinball Seth scored 50,000"
- "Hey Google, ask Atlantis Pinball who has the high score"

**Setup:**
1. Create Action in Google Actions Console
2. Configure intents (same as Alexa)
3. Create webhook endpoint
4. Handle Dialogflow requests

---

### **3. SMS/Text Input**

**Service:** Twilio

**Format:** Text to dedicated number
```
"Seth 50000" → Adds score
"High score" → Gets top score
"Leaderboard" → Gets top 5
```

**Setup:**
```python
from twilio.rest import Client

@app.post("/api/sms")
async def handle_sms(request: Request):
    body = await request.form()
    message = body['Body']
    
    # Parse: "Seth 50000"
    parts = message.split()
    player = parts[0]
    score = int(parts[1])
    
    # Add to database
    add_score(player, score)
    
    # Send confirmation
    return sms_response(f"Score added: {player} - {score}")
```

---

### **4. Web Admin Panel**

**Features:**
- Add/edit/delete scores
- Manage players
- View statistics
- Export data (CSV)
- Backup/restore

**Authentication:** Simple password or OAuth

**URL:** `https://pinball.lightspeedup.com/admin`

---

### **5. Direct API**

**RESTful API for programmatic access:**

```bash
# Add score
curl -X POST https://pinball.lightspeedup.com/api/scores \
  -H "Content-Type: application/json" \
  -d '{"player": "Seth", "score": 50000}'

# Get leaderboard
curl https://pinball.lightspeedup.com/api/leaderboard

# Get player stats
curl https://pinball.lightspeedup.com/api/players/Seth
```

---

## 🖥️ **DISPLAY OPTIONS**

### **Option A: Raspberry Pi + Vertical Monitor**

**Hardware:**
- Raspberry Pi 4 (4GB+)
- 24" or 27" monitor (rotated 90°)
- HDMI cable
- Wall mount or stand

**Setup:**
```bash
# Rotate display 90°
sudo nano /boot/config.txt
# Add: display_rotate=1

# Auto-start Chromium in kiosk mode
sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
# Add:
@chromium-browser --kiosk --app=https://pinball.lightspeedup.com/display
```

**Cost:** ~$120 (Pi + monitor)

---

### **Option B: Old Laptop + Monitor (HDMI)**

**Setup:**
- Old laptop running Linux/Windows
- Connect to vertical monitor via HDMI
- Set monitor to portrait mode
- Auto-start browser in fullscreen

**Cost:** $0 (use existing hardware)

---

### **Option C: Cast to TV**

**Setup:**
- Open browser on any device
- Cast to TV (Chromecast, Fire Stick)
- Rotate TV 90° (if possible) or design horizontal layout

**Cost:** $20-30 (if need Chromecast)

---

### **Option D: Dell Server + Browser Access**

**Setup:**
- Access from any computer/tablet
- Navigate to URL
- Press F11 for fullscreen
- Connect to external display

**Cost:** $0 (use existing infrastructure)

---

## 🏢 **LIGHTSPEEDUP INTEGRATION**

### **Hosting Strategy**

**Subdomain:** `pinball.lightspeedup.com`  
**Purpose:** Atlantis Pinball Leaderboard

**Infrastructure:**
```
Dell R730 Server (192.168.12.180)
    ↓
Docker Container: atlantis-pinball
    ↓
FastAPI Backend (Port 8000)
    ↓
React Frontend (Served by FastAPI)
    ↓
PostgreSQL Database
    ↓
Redis (Caching & Websockets)
    ↓
Nginx Reverse Proxy
    ↓
SSL: Cloudflare
```

### **Database Schema**

```sql
-- Players table
CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Scores table
CREATE TABLE scores (
    id SERIAL PRIMARY KEY,
    player_id INTEGER REFERENCES players(id),
    score INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verified BOOLEAN DEFAULT FALSE,
    photo_url VARCHAR(255)
);

-- High scores view (for quick access)
CREATE VIEW leaderboard AS
SELECT 
    RANK() OVER (ORDER BY max_score DESC) as rank,
    p.name,
    MAX(s.score) as max_score,
    COUNT(s.id) as games_played,
    AVG(s.score) as avg_score
FROM players p
JOIN scores s ON p.id = s.player_id
GROUP BY p.id, p.name
ORDER BY max_score DESC;
```

---

## 📂 **FILE STRUCTURE**

```
/home/mgmt1/GitHub/Atlantis-Pinball-Leaderboard/
├── docs/
│   └── DEVELOPMENT-HANDOVER.md      ← YOU ARE HERE
├── src/
│   ├── frontend/                    ← React app
│   │   ├── components/
│   │   │   ├── Leaderboard.jsx     ← Main display
│   │   │   ├── ScoreEntry.jsx      ← Add score form
│   │   │   ├── PlayerCard.jsx      ← Individual player
│   │   │   └── TronBackground.jsx  ← Animated BG
│   │   ├── styles/
│   │   │   ├── tron.css            ← Tron aesthetic
│   │   │   └── animations.css      ← Effects
│   │   ├── App.jsx
│   │   └── index.jsx
│   ├── backend/                     ← FastAPI
│   │   ├── main.py                 ← API routes
│   │   ├── database.py             ← DB connection
│   │   ├── models.py               ← Data models
│   │   ├── websockets.py           ← Real-time
│   │   ├── alexa.py                ← Alexa integration
│   │   └── google_assistant.py     ← Google integration
│   └── shared/
│       └── constants.py            ← Shared config
├── deployment/
│   ├── docker-compose.yml          ← Docker setup
│   ├── Dockerfile                  ← Container image
│   ├── setup-pi.sh                 ← Pi setup script
│   └── nginx.conf                  ← Reverse proxy
├── assets/
│   ├── WHITEBOARD-DATA.md          ← Current scores
│   ├── whiteboard-photo-1.jpg      ← Photo 1
│   ├── whiteboard-photo-2.jpg      ← Photo 2
│   ├── whiteboard-photo-3.jpg      ← Photo 3
│   └── atlantis-pinball-ref.jpg    ← Machine photo
├── README.md
└── .env.example                    ← Config template
```

---

## 🚀 **DEPLOYMENT STRATEGY**

### **Phase 1: MVP (Week 1)**

**Goal:** Basic leaderboard display

1. Set up FastAPI backend
2. Create React frontend with Tron styling
3. Implement basic CRUD (Create, Read, Update, Delete)
4. Deploy to Docker on Dell server
5. Test on laptop → HDMI → monitor

**Features:**
- Display top 25 scores
- Web form to add scores
- Basic Tron aesthetic
- Responsive design

---

### **Phase 2: Enhanced (Weeks 2-3)**

**Goal:** Add input methods

1. Mobile-optimized score entry
2. Real-time updates (websockets)
3. Alexa skill integration
4. Google Assistant action
5. Deploy to Raspberry Pi

**Features:**
- Voice commands working
- Mobile web app (PWA)
- Auto-refresh display
- Player statistics

---

### **Phase 3: Advanced (Month 2)**

**Goal:** Polish and extras

1. SMS integration (Twilio)
2. Achievement system
3. Photo verification
4. Admin dashboard
5. Historical statistics

---

## 🎯 **NEXT STEPS**

### **Immediate (Today):**
1. ✅ Handover document created
2. ✅ Whiteboard data extracted
3. ⏳ Review with Seth
4. ⏳ Choose tech stack (recommend React + FastAPI)
5. ⏳ Set up development environment

### **This Week:**
1. Initialize Git repository
2. Set up project structure
3. Create database schema
4. Build basic frontend (leaderboard display)
5. Build basic backend (API routes)
6. Import current scores from whiteboard

### **Next Week:**
1. Add Tron styling and animations
2. Set up vertical display (Pi or laptop)
3. Implement real-time updates
4. Create mobile score entry form
5. Deploy to Docker on server

### **Month 1:**
1. Add voice integration (Alexa + Google)
2. Add SMS integration
3. Polish UI/UX
4. Test with friends
5. Gather feedback and iterate

---

## 🔐 **SECURITY CONSIDERATIONS**

### **Public vs Private**
- **Public:** Leaderboard display (read-only)
- **Authenticated:** Score entry (registered players)
- **Admin:** Seth only (full control)

### **Authentication Options**
- **Simple:** Password-protected admin
- **OAuth:** Google/Discord login for players
- **API Keys:** For voice assistants

### **Rate Limiting**
- Max 10 score submissions per player per hour
- Prevent spam/cheating

---

## 🎨 **DESIGN MOCKUP**

```
┏━━━━━━━━━━━━━━━━━━━━━┓
┃                     ┃
┃    ▀▄▀▄▀▄▀▄▀▄      ┃  ← Tron grid animation
┃                     ┃
┃   ATLANTIS          ┃  ← Glowing title
┃   PINBALL           ┃     Cyan neon
┃   HIGH SCORES       ┃
┃                     ┃
┣━━━━━━━━━━━━━━━━━━━━━┫
┃                     ┃
┃  ╔═══════════════╗  ┃
┃  ║  🏆 KENLEY    ║  ┃  ← #1 - Extra large
┃  ║    76,590     ║  ┃     Gold outline
┃  ╚═══════════════╝  ┃     Pulsing glow
┃                     ┃
┃  ┌───────────────┐  ┃
┃  │  🥈 JASON     │  ┃  ← #2 - Large
┃  │    77,750     │  ┃     Silver outline
┃  └───────────────┘  ┃
┃                     ┃
┃  ┌───────────────┐  ┃
┃  │  🥉 ELYSE     │  ┃  ← #3 - Large
┃  │    75,340     │  ┃     Bronze outline
┃  └───────────────┘  ┃
┃                     ┃
┃  #4  DUSTIN  72390  ┃  ← Rest - Medium
┃  #5  TED     66260  ┃     Cyan text
┃  #6  SETH    66240  ┃     Orange scores
┃  #7  MIKE    61450  ┃
┃  ...                ┃
┃                     ┃
┣━━━━━━━━━━━━━━━━━━━━━┫
┃                     ┃
┃  ⚡ LATEST GAME     ┃  ← Ticker
┃  SETH - 45,000      ┃     Scrolling
┃  2 MINUTES AGO      ┃     Orange flash
┃                     ┃
┗━━━━━━━━━━━━━━━━━━━━━┛

  ▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄    ← Animated grid
```

---

## 🦅 **SEMPER FI**

This project combines:
- **Nostalgia:** 1975 pinball meets 1982 Tron
- **Technology:** Modern web stack with cutting-edge design
- **Community:** Friends competing and having fun
- **Craftsmanship:** Attention to detail in every pixel

**Build something that looks as cool as it functions.** 🎮💙

---

**Last Updated:** 2025-11-03  
**Document Version:** 1.0  
**Maintained By:** Seth Schultz, USMC Veteran  
**Related Project:** LightSpeedUp Hosting (https://lightspeedup.com)


