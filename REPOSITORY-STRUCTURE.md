# 📂 Repository Structure

**Multi-Project Repository for Family & Friends Applications**

---

## 🌳 Directory Tree

```
Family-Care-Ideas/
│
├── 📄 README.md                     ← Landing page (you are here on GitHub)
├── 📄 SETUP-GUIDE.md                ← Complete setup instructions
├── 📄 REPOSITORY-STRUCTURE.md       ← This file
├── 📄 CONTRIBUTING.md               ← Contribution guidelines
├── 📄 SECURITY.md                   ← Security policy
├── 📄 LICENSE                       ← Apache 2.0 license
├── 📄 .gitignore                    ← Protects sensitive data
│
└── 📁 projects/                     ← All projects live here
    │
    ├── 📁 atlantis-pinball-leaderboard/
    │   ├── 📄 README.md              ← Project overview
    │   ├── 📄 QUICK-START.md         ← 5-minute setup
    │   ├── 📄 DEPLOYMENT-CHECKLIST.md
    │   ├── 📄 PROJECT-SUMMARY.md
    │   ├── 📄 .env.example           ← Config template (safe)
    │   ├── 🚫 .env                   ← YOUR CONFIG (git-ignored)
    │   │
    │   ├── 📁 src/
    │   │   ├── 📁 backend/           ← Python FastAPI
    │   │   │   ├── main.py
    │   │   │   ├── models.py
    │   │   │   ├── database.py
    │   │   │   ├── websockets.py
    │   │   │   ├── email_notifications.py
    │   │   │   ├── seed_data.py
    │   │   │   └── requirements.txt
    │   │   │
    │   │   └── 📁 frontend/          ← React + Vite
    │   │       ├── src/
    │   │       ├── package.json
    │   │       └── vite.config.js
    │   │
    │   ├── 📁 deployment/            ← Docker setup
    │   │   ├── docker-compose.yml
    │   │   ├── Dockerfile.backend
    │   │   ├── Dockerfile.frontend
    │   │   ├── nginx.conf
    │   │   └── setup.sh
    │   │
    │   ├── 📁 assets/                ← Data, images
    │   │   └── WHITEBOARD-DATA.md
    │   │
    │   └── 🚫 data/                  ← Database files (git-ignored)
    │       └── atlantis_pinball.db
    │
    └── 📁 family-care-dashboard/
        ├── 📄 README.md              ← Project overview
        ├── 📁 deployment/
        ├── 📁 docs/
        └── 📁 src/
```

---

## 🎯 Project Status

### ✅ Atlantis Pinball Leaderboard
**Status:** Production Ready  
**Version:** 1.0.0  
**Technology:** FastAPI + React + Docker  
**Features:**
- Real-time score tracking
- Email notifications
- Tron aesthetic design
- Mobile-optimized input
- Admin panel

**Quick Start:**
```bash
cd projects/atlantis-pinball-leaderboard/deployment
./setup.sh
```

### 🚧 Family Care Dashboard
**Status:** In Development  
**Version:** 0.x  
**Technology:** TBD (MagicMirror² or Custom React)  
**Planned Features:**
- Google Calendar sync
- Voice commands
- Elder-friendly display
- Weather integration

---

## 🔒 Security & Privacy

### Protected Files (Git-Ignored)

These files are **NEVER** committed to GitHub:

```
🚫 .env                          ← Your passwords & API keys
🚫 *.db                          ← Database files
🚫 data/                         ← User data
🚫 *.key, *.pem                  ← SSL certificates
🚫 secrets/                      ← Any secrets directory
🚫 node_modules/                 ← Dependencies
🚫 __pycache__/                  ← Python cache
```

### Safe to Commit

```
✅ .env.example                  ← Template only (no real passwords)
✅ src/                          ← All source code
✅ *.md files                    ← Documentation
✅ docker-compose.yml            ← Configuration (no secrets)
✅ Dockerfile                    ← Build instructions
```

---

## 📝 Documentation Files

### Repository Level

| File | Purpose |
|------|---------|
| `README.md` | Landing page, project overview |
| `SETUP-GUIDE.md` | Complete setup instructions |
| `REPOSITORY-STRUCTURE.md` | This file - repo organization |
| `CONTRIBUTING.md` | How to contribute |
| `SECURITY.md` | Security policy & reporting |
| `LICENSE` | Apache 2.0 license |

### Project Level

Each project has:

| File | Purpose |
|------|---------|
| `README.md` | Project overview & features |
| `QUICK-START.md` | 5-minute setup guide |
| `DEPLOYMENT-CHECKLIST.md` | Production deployment steps |
| `PROJECT-SUMMARY.md` | Complete project details |
| `.env.example` | Configuration template |

---

## 🚀 Adding New Projects

To add a new project to this repository:

### 1. Create Project Directory

```bash
mkdir -p projects/your-new-project
cd projects/your-new-project
```

### 2. Required Files

Create these essential files:

```bash
touch README.md
touch QUICK-START.md
touch .env.example
```

### 3. Project Structure

Follow this template:

```
projects/your-new-project/
├── README.md                   ← Required
├── QUICK-START.md              ← Recommended
├── .env.example                ← If using secrets
├── src/                        ← Source code
├── deployment/                 ← Docker setup
│   ├── docker-compose.yml
│   └── Dockerfile
└── assets/                     ← Images, data
```

### 4. Update Root README

Add your project to the main README.md:

```markdown
### 🎯 [Your Project Name](./projects/your-new-project/)
**Brief description**

- Feature 1
- Feature 2

**Status:** 🚧 In Development  
**Get Started:** [Your Project →](./projects/your-new-project/)
```

### 5. Update .gitignore

Add project-specific ignore patterns:

```bash
# Your New Project
projects/your-new-project/data/
projects/your-new-project/.env
```

---

## 🎨 Design Philosophy

### Multi-Project Repository

**Why?** Keep related family projects together:
- ✅ Single clone for all projects
- ✅ Shared documentation & guidelines
- ✅ Consistent security practices
- ✅ Easier to discover related projects

### Clear Separation

**How?** Each project is independent:
- ✅ Own `src/` directory
- ✅ Own documentation
- ✅ Own deployment config
- ✅ Can be used standalone

---

## 🔄 Workflow

### Development

```bash
# Clone repository
git clone https://github.com/MatoTeziTanka/Family-Care-Ideas.git
cd Family-Care-Ideas

# Work on specific project
cd projects/atlantis-pinball-leaderboard

# Make changes
# Test locally
# Commit & push
```

### Deployment

```bash
# On production server
git pull origin main
cd projects/atlantis-pinball-leaderboard
docker-compose restart
```

---

## 📦 Technologies Used

### Backend
- **Python** - FastAPI, uvicorn
- **Database** - SQLite (development), PostgreSQL (production)
- **WebSocket** - Real-time updates

### Frontend
- **React** - UI framework
- **Vite** - Build tool
- **CSS3** - Styling & animations

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Reverse proxy
- **Git** - Version control

---

## 🤝 Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for:
- Code standards
- Pull request process
- Development guidelines

---

## 📄 License

All projects use **Apache License 2.0**:
- ✅ Free to use
- ✅ Free to modify
- ✅ Free to distribute
- ✅ Commercial use allowed
- ✅ Patent protection included

See [LICENSE](./LICENSE) for full text.

---

## 💬 Support

### Documentation
1. Check project README
2. Review SETUP-GUIDE.md
3. Read project-specific docs

### Community
- **Issues:** GitHub Issues
- **Discussions:** GitHub Discussions

### Security
- **Email:** AtlantisPinball@lightspeedup.com
- See [SECURITY.md](./SECURITY.md)

---

**Repository maintained by Seth Schultz, USMC Veteran** 🦅

---

**Last Updated:** November 3, 2025  
**Repository:** https://github.com/MatoTeziTanka/Family-Care-Ideas

