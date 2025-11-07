# 🚀 Setup Guide - Family & Friends Projects

Complete setup instructions for all projects in this repository.

---

## 📋 Prerequisites

All projects require:
- **Docker** & **Docker Compose** (recommended)
- **Git** (for cloning repository)

Individual projects may also require:
- **Python 3.11+** (backend development)
- **Node.js 18+** (frontend development)

---

## ⚡ Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/MatoTeziTanka/Family-Care-Ideas.git
cd Family-Care-Ideas
```

### 2. Choose Your Project

Navigate to the project you want to set up:

```bash
# For Atlantis Pinball Leaderboard
cd projects/atlantis-pinball-leaderboard

# For Family Care Dashboard
cd projects/family-care-dashboard
```

### 3. Follow Project-Specific Setup

Each project has its own complete documentation:
- `README.md` - Project overview and features
- `QUICK-START.md` - Fast 5-minute setup
- `DEPLOYMENT-CHECKLIST.md` - Production deployment

---

## 🎮 Atlantis Pinball Leaderboard

### Quick Setup (5 minutes)

```bash
cd projects/atlantis-pinball-leaderboard

# Configure environment (optional)
cp .env.example .env
# Edit .env with your SMTP_PASSWORD for email notifications

# Run automated setup
cd deployment
chmod +x setup.sh
./setup.sh
```

### Access Points

After setup completes:
- **Display:** http://localhost:3000
- **Add Score:** http://localhost:3000/add
- **Admin Panel:** http://localhost:3000/admin
- **API Docs:** http://localhost:8000/docs

### Email Notifications

To enable email notifications when scores are added:

1. Get Gmail App Password:
   - Go to https://myaccount.google.com/security
   - Enable 2-Step Verification
   - Generate App Password for "Mail"

2. Add to `.env` file:
```bash
SMTP_PASSWORD=your_16_character_app_password
NOTIFICATION_EMAIL=AtlantisPinball@lightspeedup.com
```

3. Restart services:
```bash
docker-compose restart
```

---

## 🏥 Family Care Dashboard

### Status: 🚧 In Development

Setup instructions coming soon!

---

## 🔒 Security Configuration

### Important: Protect Sensitive Data

**Before pushing to GitHub:**

1. **Never commit** `.env` files with real passwords
2. **Always use** `.env.example` with placeholder values
3. **Check** `.gitignore` includes sensitive files
4. **Review** commits before pushing

### Files to Keep Private

❌ Never commit:
- `.env` (contains passwords)
- `*.db` (database files)
- `data/` directory
- Any files with API keys or tokens

✅ Safe to commit:
- `.env.example` (template only)
- All source code
- Documentation
- Configuration templates

---

## 🐳 Docker Commands

### View Status
```bash
docker-compose ps
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Restart Services
```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart backend
```

### Stop Services
```bash
docker-compose down
```

### Rebuild (after code changes)
```bash
docker-compose build
docker-compose up -d
```

---

## 🛠️ Development Setup

### Backend Development (Python)

```bash
cd projects/[project-name]/src/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python main.py
```

### Frontend Development (React)

```bash
cd projects/[project-name]/src/frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

---

## 🌐 Production Deployment

### On Dell R730 Server (or any Linux server)

1. **Install Docker:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

2. **Install Docker Compose:**
```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

3. **Clone and Deploy:**
```bash
git clone https://github.com/MatoTeziTanka/Family-Care-Ideas.git
cd Family-Care-Ideas/projects/[project-name]
cp .env.example .env
# Edit .env with production values
cd deployment
./setup.sh
```

4. **Configure SSL (Production):**
```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com

# Enable auto-renewal
sudo certbot renew --dry-run
```

---

## 🐛 Troubleshooting

### Port Already in Use

If you see "port already in use" errors:

1. Check what's using the port:
```bash
sudo lsof -i :8000  # Backend port
sudo lsof -i :3000  # Frontend port
```

2. Edit `docker-compose.yml` to use different ports:
```yaml
ports:
  - "8001:8000"  # Changed from 8000:8000
```

### Database Locked

If you see "database is locked" errors:
- SQLite doesn't handle concurrent writes well
- Consider PostgreSQL for production
- Ensure only one backend instance is running

### WebSocket Not Connecting

1. Check firewall allows WebSocket connections
2. Verify nginx WebSocket proxy configuration
3. Check browser console for errors

### Email Not Sending

1. Verify SMTP_PASSWORD is correct (16 characters, no spaces)
2. Check Gmail account has 2-Step Verification enabled
3. Verify app password is active (not revoked)
4. Check backend logs: `docker-compose logs backend`

---

## 📖 Documentation Structure

Each project follows this structure:

```
projects/[project-name]/
├── README.md                   ← Project overview
├── QUICK-START.md              ← 5-minute setup
├── DEPLOYMENT-CHECKLIST.md     ← Production deployment
├── PROJECT-SUMMARY.md          ← Complete project details
├── .env.example                ← Configuration template
├── src/                        ← Source code
├── deployment/                 ← Docker setup
└── assets/                     ← Images, data, etc.
```

---

## 💬 Getting Help

### Documentation
- Check project README files
- Review QUICK-START guides
- Read DEPLOYMENT-CHECKLIST

### Issues
- **GitHub Issues:** https://github.com/MatoTeziTanka/Family-Care-Ideas/issues
- **Discussions:** https://github.com/MatoTeziTanka/Family-Care-Ideas/discussions

### Security Issues
- **Email:** AtlantisPinball@lightspeedup.com
- See [SECURITY.md](./SECURITY.md)

---

## ⭐ Next Steps

After successful setup:

1. ✅ Test all features
2. ✅ Configure for your needs
3. ✅ Set up backups (important!)
4. ✅ Star the repository
5. ✅ Share with others who might benefit

---

**Built by families, for families. Privacy-first. Always free.** 🦅

---

**Last Updated:** November 3, 2025



