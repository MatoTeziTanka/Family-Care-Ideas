# 🚀 QUICK START GUIDE

Get your Atlantis Pinball Leaderboard running in **5 minutes**!

---

## ⚡ One-Command Setup

```bash
# From the Family-Care-Ideas repository root:
cd projects/atlantis-pinball-leaderboard/deployment
chmod +x setup.sh
./setup.sh
```

That's it! The script will:
1. ✅ Install Python dependencies
2. ✅ Seed database with 25 players
3. ✅ Build Docker containers
4. ✅ Start all services
5. ✅ Run health checks

---

## 📍 Access Your Leaderboard

Once setup completes, visit:

### **Main Display (Vertical View)**
```
http://localhost:3000
```
Perfect for arcade cabinet, vertical monitor, or TV display

### **Add Score (Mobile)**
```
http://localhost:3000/add
```
Mobile-optimized touch interface for score entry

### **Admin Panel**
```
http://localhost:3000/admin
```
Manage scores and view statistics

### **API Documentation**
```
http://localhost:8000/docs
```
Interactive API documentation (Swagger UI)

---

## 🎮 Testing the System

### 1. View Leaderboard
Open `http://localhost:3000` in your browser to see all 25 players

### 2. Add a Test Score
1. Navigate to `http://localhost:3000/add`
2. Select a player (e.g., "Seth")
3. Enter a score (e.g., 80000)
4. Click "SUBMIT SCORE"
5. Watch the main display update in real-time! ⚡

### 3. Check WebSocket Connection
Open browser console on display page, you should see:
```
✅ WebSocket connected
📡 Broadcast to X clients: new_score
```

---

## 🐳 Docker Commands

### View Running Containers
```bash
docker-compose ps
```

### View Logs
```bash
# All services
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Frontend only
docker-compose logs -f frontend
```

### Restart Services
```bash
docker-compose restart
```

### Stop Services
```bash
docker-compose down
```

### Rebuild Containers
```bash
docker-compose build --no-cache
docker-compose up -d
```

---

## 🛠️ Manual Setup (Without Docker)

### Backend

```bash
cd src/backend

# Install dependencies
pip install -r requirements.txt

# Seed database
python seed_data.py

# Run server
python main.py
# or
uvicorn main:app --reload --port 8000
```

Backend runs at `http://localhost:8000`

### Frontend

```bash
cd src/frontend

# Install dependencies
npm install

# Run dev server
npm run dev
```

Frontend runs at `http://localhost:3000`

---

## 📱 Display on Different Devices

### Raspberry Pi (Vertical Monitor)

1. **SSH into Raspberry Pi:**
```bash
ssh pi@raspberrypi.local
```

2. **Install Chromium:**
```bash
sudo apt-get update
sudo apt-get install chromium-browser
```

3. **Rotate Display:**
Edit `/boot/config.txt`:
```bash
sudo nano /boot/config.txt
# Add:
display_rotate=1  # 90° clockwise
```

4. **Auto-start Browser:**
Edit autostart:
```bash
sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
# Add:
@chromium-browser --kiosk --app=http://pinball.lightspeedup.com
```

5. **Reboot:**
```bash
sudo reboot
```

### Cast to TV

1. Open Chrome browser
2. Navigate to leaderboard display
3. Click menu (⋮) → "Cast..."
4. Select your Chromecast/TV
5. Choose "Cast tab" or "Cast desktop"

### Mobile Device

1. Open browser on phone/tablet
2. Navigate to display URL
3. Add to home screen (PWA support)
4. Open in full screen

---

## 🎨 Customization

### Change Colors

Edit `src/frontend/src/styles/tron.css`:

```css
:root {
  --cyan: #00D9FF;      /* Change primary color */
  --orange: #FF9500;    /* Change secondary color */
}
```

### Add More Players

```bash
cd src/backend

# Open Python shell
python3

# Add player
>>> import asyncio
>>> from database import init_db, get_db
>>> async def add_player():
...     await init_db()
...     db = await get_db()
...     await db.execute("INSERT INTO players (name) VALUES (?)", ["NewPlayer"])
>>> asyncio.run(add_player())
```

Or use the API:
```bash
curl -X POST http://localhost:8000/api/players \
  -H "Content-Type: application/json" \
  -d '{"name": "NewPlayer"}'
```

---

## 🐛 Troubleshooting

### Port Already in Use

If ports 3000 or 8000 are already in use:

Edit `deployment/docker-compose.yml`:
```yaml
services:
  backend:
    ports:
      - "8001:8000"  # Changed from 8000:8000
  frontend:
    ports:
      - "3001:80"    # Changed from 3000:80
```

### WebSocket Not Connecting

1. Check firewall settings
2. Verify backend is running: `curl http://localhost:8000/api/health`
3. Check browser console for errors
4. Try refreshing the page

### Database Locked

SQLite can lock with concurrent writes. For production, switch to PostgreSQL:

```bash
# Install PostgreSQL
sudo apt-get install postgresql

# Update DATABASE_URL in .env
DATABASE_URL=postgresql://user:pass@localhost:5432/atlantis
```

### Display Not Updating

1. Hard refresh browser (Ctrl+Shift+R or Cmd+Shift+R)
2. Check WebSocket connection in browser console
3. Restart Docker containers: `docker-compose restart`

---

## 📊 Production Deployment

### On Dell R730 Server

1. **Clone repository:**
```bash
git clone <repo-url>
cd atlantis-pinball-leaderboard
```

2. **Run setup:**
```bash
cd deployment
./setup.sh
```

3. **Configure domain:**
Edit `deployment/nginx.conf`:
```nginx
server_name pinball.lightspeedup.com;
```

4. **Set up SSL (Let's Encrypt):**
```bash
sudo certbot --nginx -d pinball.lightspeedup.com
```

5. **Start services:**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

## 📞 Support

- **Documentation:** `/docs/DEVELOPMENT-HANDOVER.md`
- **API Docs:** `http://localhost:8000/docs`
- **Issues:** Check logs with `docker-compose logs -f`

---

## 🎮 Next Steps

1. ✅ Test the display on your vertical monitor
2. ✅ Add scores from your phone
3. ✅ Set up Raspberry Pi for dedicated display
4. 🚀 Configure voice commands (Alexa/Google)
5. 🚀 Add SMS integration
6. 🚀 Enable photo verification

---

**🎮 Semper Fi! Enjoy your Tron-themed leaderboard!** 💙

---

**Last Updated:** November 3, 2025

