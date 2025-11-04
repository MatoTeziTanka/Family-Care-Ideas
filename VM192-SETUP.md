# 🖥️ VM192 (Personal) - Complete Setup Guide

**VM Name:** Personal  
**Current IP:** 192.168.12.190  
**Target IP:** 192.168.12.192  
**MAC (last 4):** b766  
**Current User:** future1  
**New User:** admin  
**Purpose:** Host personal projects (Atlantis Pinball, Family Care, etc.)

---

## 🚀 Quick Setup

SSH into the VM and run these commands:

```bash
ssh future1@192.168.12.190
# Password: Norelec7!
```

Then run this one-liner to download and execute the setup script:

```bash
curl -fsSL https://raw.githubusercontent.com/MatoTeziTanka/Family-Care-Ideas/main/vm-setup.sh | sudo bash
```

Or follow the manual steps below.

---

## 📋 Manual Setup Steps

### Step 1: Initial Connection & Verification

```bash
# SSH into VM
ssh future1@192.168.12.190
# Password: Norelec7!

# Verify current state
echo "=== Current Configuration ==="
hostname
ip addr show | grep "inet "
cat /sys/class/net/*/address | grep -i "b766"
uname -a
df -h
free -h
```

**Expected output:**
- Hostname: Something generic (not "personal" yet)
- IP: 192.168.12.190
- MAC ending in: b766
- OS: Ubuntu Server (likely)

---

### Step 2: System Update

```bash
# Update package lists
sudo apt update

# Upgrade all packages
sudo apt upgrade -y

# Install essential tools
sudo apt install -y \
    net-tools \
    curl \
    wget \
    git \
    nano \
    vim \
    htop \
    ufw \
    fail2ban \
    unattended-upgrades
```

---

### Step 3: Change Hostname to "personal"

```bash
# Set new hostname
sudo hostnamectl set-hostname personal

# Update /etc/hosts
sudo nano /etc/hosts
```

**Edit /etc/hosts to include:**
```
127.0.0.1       localhost
127.0.1.1       personal
192.168.12.192  personal

# Keep other lines as-is
```

**Verify:**
```bash
hostnamectl
# Should show: Static hostname: personal
```

---

### Step 4: Change IP to 192.168.12.192 (Static)

First, identify your network interface:
```bash
ip addr show
# Look for the interface name (likely ens160, ens192, eth0, etc.)
```

#### For Netplan (Ubuntu 18.04+):

```bash
# Find netplan config
ls /etc/netplan/

# Edit the config file
sudo nano /etc/netplan/00-installer-config.yaml
```

**Replace with:**
```yaml
network:
  version: 2
  ethernets:
    ens160:  # Replace with your actual interface name
      dhcp4: no
      addresses:
        - 192.168.12.192/24
      gateway4: 192.168.12.1
      nameservers:
        addresses:
          - 8.8.8.8
          - 1.1.1.1
      match:
        macaddress: "XX:XX:XX:XX:b7:66"  # Use your full MAC
      set-name: ens160
```

**Apply changes:**
```bash
sudo netplan apply

# Verify new IP
ip addr show | grep "inet 192.168.12.192"
```

⚠️ **WARNING:** Your SSH session will disconnect! Reconnect with:
```bash
ssh future1@192.168.12.192
```

---

### Step 5: Create New Admin User

```bash
# Create new user with home directory
sudo adduser admin
# Set password: [Choose a strong password]

# Add to sudo group
sudo usermod -aG sudo admin

# Add to docker group (for later)
sudo usermod -aG docker admin

# Verify groups
groups admin
# Should show: admin sudo docker
```

**Test new user:**
```bash
# Open NEW terminal window
ssh admin@192.168.12.192

# Test sudo access
sudo whoami
# Should output: root

# If successful, leave this session open and continue
```

---

### Step 6: Configure SSH for Admin User

```bash
# As admin user
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Copy authorized_keys from future1 (if exists)
sudo cp /home/future1/.ssh/authorized_keys ~/.ssh/ 2>/dev/null || echo "No keys to copy"
sudo chown admin:admin ~/.ssh/authorized_keys 2>/dev/null
chmod 600 ~/.ssh/authorized_keys 2>/dev/null

# Generate new SSH key pair (optional, for future use)
ssh-keygen -t ed25519 -C "admin@personal"
```

---

### Step 7: Configure Firewall (UFW)

```bash
# Check current status
sudo ufw status

# Allow SSH (IMPORTANT - do this first!)
sudo ufw allow 22/tcp

# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Allow application ports
sudo ufw allow 3000/tcp  # Frontend
sudo ufw allow 8000/tcp  # Backend API

# Enable firewall
sudo ufw enable

# Verify
sudo ufw status verbose
```

**Expected output:**
```
Status: active

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW       Anywhere
80/tcp                     ALLOW       Anywhere
443/tcp                    ALLOW       Anywhere
3000/tcp                   ALLOW       Anywhere
8000/tcp                   ALLOW       Anywhere
```

---

### Step 8: Install Docker & Docker Compose

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add admin to docker group
sudo usermod -aG docker admin

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Enable Docker service
sudo systemctl enable docker
sudo systemctl start docker

# Verify installation
docker --version
docker-compose --version
```

**Logout and login again for group changes to take effect:**
```bash
exit
ssh admin@192.168.12.192
```

**Test Docker:**
```bash
docker run hello-world
# Should download and run successfully
```

---

### Step 9: Full System Scan

```bash
# Check OS version
cat /etc/os-release

# Check kernel version
uname -r

# List installed packages
dpkg -l | wc -l  # Total count
dpkg -l | less   # Browse all packages

# Check running services
systemctl list-units --type=service --state=running

# Check disk usage
df -h

# Check memory usage
free -h

# Check open ports
sudo netstat -tlnp

# List all users
cat /etc/passwd | grep -v "nologin\|false" | cut -d: -f1

# Check for unnecessary packages
sudo apt autoremove --dry-run
```

**Document findings:**
```bash
# Create system info file
cat > ~/system-info.txt << 'EOF'
=== VM192 (Personal) System Information ===
Date: $(date)
Hostname: $(hostname)
OS: $(cat /etc/os-release | grep PRETTY_NAME)
Kernel: $(uname -r)
IP: $(ip -4 addr show | grep inet | grep -v 127.0.0.1 | awk '{print $2}')
MAC: $(cat /sys/class/net/*/address | grep b766)
Memory: $(free -h | grep Mem | awk '{print $2}')
Disk: $(df -h / | tail -1 | awk '{print $2}')
Docker: $(docker --version)
EOF

cat ~/system-info.txt
```

---

### Step 10: Remove Unnecessary Software

```bash
# List snap packages
snap list

# Remove unused snaps (if any)
# sudo snap remove <package-name>

# Remove orphaned packages
sudo apt autoremove -y

# Clean package cache
sudo apt clean
```

---

### Step 11: Install Fail2Ban (Security)

```bash
# Install fail2ban
sudo apt install -y fail2ban

# Create local config
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local

# Edit config
sudo nano /etc/fail2ban/jail.local
```

**Find and update these settings:**
```ini
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3

[sshd]
enabled = true
port = 22
```

**Restart fail2ban:**
```bash
sudo systemctl restart fail2ban
sudo systemctl enable fail2ban
sudo fail2ban-client status
```

---

### Step 12: Configure Automatic Security Updates

```bash
# Configure unattended-upgrades
sudo nano /etc/apt/apt.conf.d/50unattended-upgrades
```

**Ensure these lines are uncommented:**
```
Unattended-Upgrade::Allowed-Origins {
    "${distro_id}:${distro_codename}-security";
};
Unattended-Upgrade::Automatic-Reboot "false";
```

**Enable automatic updates:**
```bash
sudo dpkg-reconfigure -plow unattended-upgrades
# Select "Yes"
```

---

### Step 13: Delete future1 User

⚠️ **ONLY do this after validating admin user works!**

```bash
# Verify you're logged in as admin
whoami
# Should output: admin

# Kill any future1 processes
sudo pkill -u future1

# Delete future1 user and home directory
sudo deluser --remove-home future1

# Verify deletion
cat /etc/passwd | grep future1
# Should return nothing
```

---

### Step 14: Deploy Family Care Projects

```bash
# Clone repository
cd ~
git clone https://github.com/MatoTeziTanka/Family-Care-Ideas.git
cd Family-Care-Ideas

# Set up Atlantis Pinball
cd projects/atlantis-pinball-leaderboard

# Create .env file
cp .env.example .env
nano .env
```

**Add to .env:**
```bash
# Email Configuration
SMTP_USERNAME=lightspeedup.smtp@gmail.com
SMTP_PASSWORD=your_gmail_app_password_here
NOTIFICATION_EMAIL=AtlantisPinball@lightspeedup.com

# Database
DATABASE_URL=sqlite:///data/atlantis_pinball.db

# API
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=*

# Frontend
VITE_API_URL=http://192.168.12.192:8000
VITE_WS_URL=ws://192.168.12.192:8000/ws
```

**Deploy:**
```bash
cd deployment
./setup.sh
```

**Verify deployment:**
```bash
docker-compose ps
# Should show running containers

# Check logs
docker-compose logs -f
```

**Access URLs:**
- Display: http://192.168.12.192:3000
- Add Score: http://192.168.12.192:3000/add
- Admin: http://192.168.12.192:3000/admin
- API Docs: http://192.168.12.192:8000/docs

---

## 📊 Post-Setup Verification Checklist

```bash
# Run this comprehensive check
cat << 'EOF' | sudo bash
#!/bin/bash
echo "==================================="
echo "VM192 (Personal) - Setup Verification"
echo "==================================="
echo ""
echo "1. Hostname:"
hostname
echo ""
echo "2. IP Address:"
ip addr show | grep "inet 192.168.12.192"
echo ""
echo "3. MAC Address (last 4 should be b766):"
ip addr show | grep "ether" | grep "b766"
echo ""
echo "4. Current User:"
whoami
echo ""
echo "5. User Groups:"
groups
echo ""
echo "6. Docker Status:"
systemctl is-active docker
docker --version
echo ""
echo "7. Firewall Status:"
ufw status | head -10
echo ""
echo "8. Fail2Ban Status:"
systemctl is-active fail2ban
echo ""
echo "9. Disk Usage:"
df -h / | tail -1
echo ""
echo "10. Memory Usage:"
free -h | grep Mem
echo ""
echo "11. Running Containers:"
docker ps --format "table {{.Names}}\t{{.Status}}"
echo ""
echo "12. Open Ports:"
ss -tlnp | grep LISTEN
echo ""
echo "==================================="
EOF
```

---

## 🔒 Security Recommendations

### Change Default Password
```bash
# Change admin password
passwd
```

### Set Up SSH Keys (More Secure)
```bash
# On your local machine (mgmt1@192.168.12.180)
ssh-keygen -t ed25519 -C "mgmt1-to-personal"

# Copy to VM
ssh-copy-id admin@192.168.12.192

# Test passwordless login
ssh admin@192.168.12.192

# Once working, disable password auth (optional)
sudo nano /etc/ssh/sshd_config
# Set: PasswordAuthentication no
sudo systemctl restart sshd
```

### Regular Updates
```bash
# Add to crontab
crontab -e

# Add this line (updates weekly on Sunday at 3 AM)
0 3 * * 0 /usr/bin/apt update && /usr/bin/apt upgrade -y
```

---

## 📝 Important Files & Locations

```
/home/admin/                          Home directory
/home/admin/Family-Care-Ideas/        Project repository
/etc/netplan/                         Network configuration
/etc/hosts                            Hostname mapping
/etc/ufw/                             Firewall rules
/etc/fail2ban/                        Intrusion prevention
/var/log/                             System logs
```

---

## 🆘 Troubleshooting

### Can't SSH After IP Change
```bash
# Connect via VM console (ESXi/Proxmox)
# Check IP configuration
ip addr show
sudo netplan apply
```

### Docker Containers Won't Start
```bash
# Check logs
docker-compose logs

# Restart Docker
sudo systemctl restart docker
```

### Firewall Blocking Connections
```bash
# Temporarily disable to test
sudo ufw disable

# If it works, add the rule you need
sudo ufw allow <port>/tcp

# Re-enable
sudo ufw enable
```

---

## 📊 Quick Reference

| Item | Value |
|------|-------|
| **Hostname** | personal |
| **IP Address** | 192.168.12.192 |
| **Gateway** | 192.168.12.1 |
| **DNS** | 8.8.8.8, 1.1.1.1 |
| **Username** | admin |
| **SSH Port** | 22 |
| **HTTP Port** | 80 |
| **HTTPS Port** | 443 |
| **Frontend Port** | 3000 |
| **Backend Port** | 8000 |

---

## ✅ Setup Complete!

Your VM192 (Personal) is now:
- ✅ Configured with hostname "personal"
- ✅ Set to static IP 192.168.12.192
- ✅ Admin user created with sudo access
- ✅ future1 user removed (after validation)
- ✅ Firewall configured and enabled
- ✅ Docker & Docker Compose installed
- ✅ Security hardened (fail2ban, auto-updates)
- ✅ Ready to host your projects!

**Next Steps:**
1. Deploy projects from Family-Care-Ideas repository
2. Configure domain names (pinball.lightspeedup.com)
3. Set up SSL certificates (Let's Encrypt)
4. Configure backups

---

**Maintained by:** Seth Schultz  
**Last Updated:** November 3, 2025  
**VM Purpose:** Personal Projects (Atlantis Pinball, Family Care Dashboard)

🦅 Semper Fi!

