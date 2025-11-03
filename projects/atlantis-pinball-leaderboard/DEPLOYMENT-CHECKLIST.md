# ✅ DEPLOYMENT CHECKLIST

Use this checklist to deploy your Atlantis Pinball Leaderboard to production.

---

## 📋 PRE-DEPLOYMENT

### 1. System Requirements
- [ ] Docker installed (`docker --version`)
- [ ] Docker Compose installed (`docker-compose --version`)
- [ ] Ports 80, 443, 3000, 8000 available
- [ ] Python 3.11+ installed (for seeding)
- [ ] Git installed (for version control)

### 2. Server Setup (Dell R730)
- [ ] Server accessible via SSH
- [ ] Firewall configured (allow ports 80, 443)
- [ ] Domain DNS configured (pinball.lightspeedup.com → server IP)
- [ ] SSL certificate ready (Let's Encrypt recommended)

---

## 🚀 DEPLOYMENT STEPS

### Step 1: Clone Repository
```bash
cd /home/mgmt1/GitHub
git clone https://github.com/MatoTeziTanka/Family-Care-Ideas.git
cd Family-Care-Ideas/projects/atlantis-pinball-leaderboard
```
- [ ] Repository cloned
- [ ] All files present

### Step 2: Database Setup
```bash
cd src/backend
pip3 install -r requirements.txt
python3 seed_data.py
```
- [ ] Python dependencies installed
- [ ] Database created at `data/atlantis_pinball.db`
- [ ] 25 players seeded
- [ ] High scores imported

### Step 3: Configuration
```bash
cd ../../deployment
```

**Edit `docker-compose.yml`:**
- [ ] Verify port mappings (80, 443, 8000, 3000)
- [ ] Update environment variables if needed

**Edit `nginx.conf`:**
- [ ] Update `server_name` to `pinball.lightspeedup.com`
- [ ] Configure SSL paths (if using HTTPS)

- [ ] Configuration files updated

### Step 4: Build Containers
```bash
docker-compose build
```
- [ ] Backend container built successfully
- [ ] Frontend container built successfully
- [ ] No build errors

### Step 5: Start Services
```bash
docker-compose up -d
```
- [ ] All containers started
- [ ] No errors in logs (`docker-compose logs`)

### Step 6: Health Check
```bash
# Check backend
curl http://localhost:8000/api/health

# Check frontend  
curl http://localhost:3000

# View running containers
docker-compose ps
```
- [ ] Backend API responding
- [ ] Frontend serving
- [ ] All containers healthy

---

## 🧪 TESTING

### Test 1: View Leaderboard
```bash
# Open browser
http://pinball.lightspeedup.com
```
- [ ] Leaderboard displays
- [ ] All 25 players visible
- [ ] Tron aesthetic loading
- [ ] Animations working
- [ ] No console errors

### Test 2: Add Score
```bash
# Navigate to score entry
http://pinball.lightspeedup.com/add
```
- [ ] Player dropdown loads
- [ ] Score input works
- [ ] Quick buttons functional
- [ ] Submit successful
- [ ] Confirmation message appears

### Test 3: Real-time Update
1. Open leaderboard in one browser window
2. Open score entry in another window
3. Submit a new score
- [ ] WebSocket connects (check console)
- [ ] Leaderboard updates automatically
- [ ] Recent score ticker updates
- [ ] No page refresh needed

### Test 4: Admin Panel
```bash
http://pinball.lightspeedup.com/admin
```
- [ ] Leaderboard tab loads
- [ ] Recent scores tab loads
- [ ] Delete button works (test with dummy score)

### Test 5: Mobile Responsive
- [ ] Test on phone/tablet
- [ ] Touch inputs work
- [ ] Readable text size
- [ ] Buttons easy to tap

---

## 📱 DISPLAY SETUP

### Option A: Raspberry Pi + Vertical Monitor

#### Hardware Setup
- [ ] Raspberry Pi 4 (4GB+) powered on
- [ ] Monitor connected via HDMI
- [ ] Monitor physically rotated 90° clockwise
- [ ] Power and network connected

#### Software Setup
```bash
# SSH to Pi
ssh pi@raspberrypi.local

# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Chromium
sudo apt-get install chromium-browser -y
```
- [ ] System updated
- [ ] Chromium installed

#### Display Rotation
```bash
# Edit boot config
sudo nano /boot/config.txt

# Add this line:
display_rotate=1

# Save and reboot
sudo reboot
```
- [ ] Display rotated to portrait
- [ ] Orientation correct

#### Kiosk Mode
```bash
# Edit autostart
sudo nano /etc/xdg/lxsession/LXDE-pi/autostart

# Add these lines:
@xset s off
@xset -dpms
@xset s noblank
@chromium-browser --kiosk --app=http://pinball.lightspeedup.com

# Reboot
sudo reboot
```
- [ ] Browser auto-starts
- [ ] Full-screen mode
- [ ] No mouse cursor
- [ ] Screen doesn't sleep

### Option B: Laptop/Desktop + Monitor
- [ ] Connect via HDMI
- [ ] Set display to portrait mode in OS settings
- [ ] Open browser to leaderboard URL
- [ ] Press F11 for fullscreen
- [ ] Configure to auto-start on boot

### Option C: Cast to TV
- [ ] Chromecast/Fire Stick connected to TV
- [ ] Open Chrome browser
- [ ] Cast tab to TV
- [ ] Consider rotating TV if possible

---

## 🔐 SECURITY (Production)

### SSL/HTTPS Setup
```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d pinball.lightspeedup.com

# Auto-renewal
sudo certbot renew --dry-run
```
- [ ] SSL certificate obtained
- [ ] HTTPS working
- [ ] HTTP redirects to HTTPS
- [ ] Auto-renewal configured

### Firewall
```bash
# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```
- [ ] Firewall configured
- [ ] Ports 80/443 open
- [ ] Other ports blocked

### Admin Access
- [ ] Admin panel password-protected (Phase 2)
- [ ] API rate limiting configured (Phase 2)
- [ ] Database backed up regularly

---

## 💾 BACKUP & MAINTENANCE

### Daily Backups
```bash
# Create backup script
cat > /home/mgmt1/backup-pinball.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d-%H%M%S)
cp /home/mgmt1/GitHub/Atlantis-Pinball-Leaderboard/data/atlantis_pinball.db \
   /home/mgmt1/backups/atlantis_pinball_${DATE}.db
# Keep only last 30 days
find /home/mgmt1/backups -name "atlantis_pinball_*.db" -mtime +30 -delete
EOF

chmod +x /home/mgmt1/backup-pinball.sh

# Add to crontab (daily at 3am)
(crontab -l 2>/dev/null; echo "0 3 * * * /home/mgmt1/backup-pinball.sh") | crontab -
```
- [ ] Backup script created
- [ ] Cron job configured
- [ ] Backup location has space
- [ ] Test restore process

### Monitoring
```bash
# Check service status
docker-compose ps

# View logs
docker-compose logs -f

# Check disk space
df -h

# Check memory
free -h
```
- [ ] Monitoring tools set up
- [ ] Log rotation configured
- [ ] Disk space monitored
- [ ] Resource usage acceptable

---

## 📊 POST-DEPLOYMENT

### Documentation
- [ ] Update README with production URL
- [ ] Document any custom configuration
- [ ] Create troubleshooting guide
- [ ] Share access URLs with friends

### Announcement
- [ ] Test all features one final time
- [ ] Take screenshots/video
- [ ] Share with pinball group
- [ ] Celebrate! 🎉

---

## 🐛 TROUBLESHOOTING

### Issue: Containers won't start
```bash
docker-compose down
docker-compose up -d
docker-compose logs
```

### Issue: WebSocket not connecting
- Check firewall allows WebSocket protocol
- Verify nginx WebSocket proxy config
- Check browser console for errors

### Issue: Database locked
- Only one process can write to SQLite
- Consider PostgreSQL for high concurrency
- Check for zombie processes

### Issue: Display not updating
- Hard refresh browser (Ctrl+Shift+R)
- Check WebSocket connection
- Verify backend is running
- Restart containers

---

## 📞 SUPPORT CONTACTS

**Technical Issues:**
- Check logs: `docker-compose logs -f`
- Review documentation: `/docs/DEVELOPMENT-HANDOVER.md`
- API docs: `http://localhost:8000/docs`

**System Administrator:**
- Seth Schultz
- USMC Veteran
- LightSpeedUp Hosting

---

## ✅ SIGN-OFF

Date Deployed: _______________

Deployed By: _______________

Production URL: `http://pinball.lightspeedup.com`

Status: 
- [ ] All systems operational
- [ ] Monitoring configured
- [ ] Backups working
- [ ] Documentation complete
- [ ] Users notified

**🎮 DEPLOYMENT COMPLETE - SEMPER FI! 🎮**

---

**Last Updated:** November 3, 2025

