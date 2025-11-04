# 🚀 VM192 Setup - Manual Steps

Since automated SCP doesn't work, follow these manual steps:

---

## Method 1: Copy/Paste Script (Easiest)

### Step 1: SSH into VM192
```bash
ssh future1@192.168.12.192
# Enter password: Norelec7!
```

### Step 2: Create the setup script
```bash
nano setup.sh
```

### Step 3: Copy and paste this entire script:

```bash
#!/bin/bash
set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}VM192 Setup Starting...${NC}"

# Check not root
if [ "$EUID" -eq 0 ]; then 
    echo -e "${RED}Run as regular user, not sudo${NC}"
    exit 1
fi

run_sudo() {
    echo -e "${YELLOW}Running: $@${NC}"
    sudo "$@"
}

# Update system
echo -e "${GREEN}Step 1: Updating system${NC}"
run_sudo apt update
run_sudo apt upgrade -y

# Install tools
echo -e "${GREEN}Step 2: Installing tools${NC}"
run_sudo apt install -y curl wget git nano vim htop ufw fail2ban unattended-upgrades rsync net-tools

# Set hostname
echo -e "${GREEN}Step 3: Setting hostname to 'personal'${NC}"
run_sudo hostnamectl set-hostname personal
echo "127.0.1.1 personal" | sudo tee -a /etc/hosts
echo "192.168.12.192 personal" | sudo tee -a /etc/hosts

# Verify IP
echo -e "${GREEN}Step 4: Verifying IP${NC}"
ip addr show | grep "inet 192.168.12.192" && echo "✅ IP correct" || echo "⚠️ Check IP"

# Create admin user
echo -e "${GREEN}Step 5: Creating admin user${NC}"
if ! id "admin" &>/dev/null; then
    run_sudo adduser --gecos "" admin
    run_sudo usermod -aG sudo admin
    echo "✅ Admin user created"
else
    echo "Admin already exists"
fi

# Install Docker
echo -e "${GREEN}Step 6: Installing Docker${NC}"
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    run_sudo sh get-docker.sh
    rm get-docker.sh
    run_sudo systemctl enable docker
    run_sudo systemctl start docker
    run_sudo usermod -aG docker $USER
    run_sudo usermod -aG docker admin 2>/dev/null || true
    echo "✅ Docker installed"
else
    echo "Docker already installed"
fi

# Install Docker Compose
echo -e "${GREEN}Step 7: Installing Docker Compose${NC}"
if ! command -v docker-compose &> /dev/null; then
    run_sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    run_sudo chmod +x /usr/local/bin/docker-compose
    echo "✅ Docker Compose installed"
fi

# Configure firewall
echo -e "${GREEN}Step 8: Configuring firewall${NC}"
run_sudo ufw --force reset
run_sudo ufw default deny incoming
run_sudo ufw default allow outgoing
run_sudo ufw allow 22/tcp
run_sudo ufw allow 80/tcp
run_sudo ufw allow 443/tcp
run_sudo ufw allow 3000/tcp
run_sudo ufw allow 8000/tcp
run_sudo ufw --force enable
echo "✅ Firewall configured"

# Configure fail2ban
echo -e "${GREEN}Step 9: Configuring fail2ban${NC}"
run_sudo systemctl enable fail2ban
run_sudo systemctl start fail2ban
echo "✅ Fail2ban enabled"

# Auto updates
echo -e "${GREEN}Step 10: Enabling auto-updates${NC}"
echo 'APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";' | sudo tee /etc/apt/apt.conf.d/20auto-upgrades > /dev/null
echo "✅ Auto-updates enabled"

# Cleanup
echo -e "${GREEN}Step 11: Cleaning up${NC}"
run_sudo apt autoremove -y
run_sudo apt clean

echo ""
echo -e "${BLUE}=== Setup Complete! ===${NC}"
echo ""
echo "Hostname: $(hostname)"
echo "IP: $(ip addr show | grep 'inet 192.168.12' | awk '{print $2}')"
echo "Docker: $(docker --version 2>/dev/null || echo 'Not found')"
echo ""
echo "Next steps:"
echo "1. Logout and login (for docker group)"
echo "2. Test admin user: ssh admin@192.168.12.192"
echo "3. Clone projects: git clone https://github.com/MatoTeziTanka/Family-Care-Ideas.git"
echo "4. Delete future1: sudo deluser --remove-home future1"
echo ""
echo "🦅 Semper Fi!"
```

### Step 4: Save and exit
- Press `Ctrl+X`
- Press `Y`
- Press `Enter`

### Step 5: Run the script
```bash
bash setup.sh
```

---

## Method 2: Download from Web (After GitHub Push)

```bash
# SSH into VM
ssh future1@192.168.12.192

# Download script
wget https://raw.githubusercontent.com/MatoTeziTanka/Family-Care-Ideas/main/vm192-complete-setup.sh -O setup.sh

# Run it
bash setup.sh
```

---

## Method 3: Use rsync (if available)

```bash
# From 192.168.12.180
rsync -avz /home/mgmt1/vm192-complete-setup.sh future1@192.168.12.192:~/
ssh future1@192.168.12.192
bash vm192-complete-setup.sh
```

---

## After Setup

Once script completes:

1. **Logout and login again:**
```bash
exit
ssh future1@192.168.12.192
```

2. **Test Docker:**
```bash
docker run hello-world
```

3. **Test admin user (NEW terminal):**
```bash
ssh admin@192.168.12.192
sudo whoami  # Should output: root
```

4. **Clone projects:**
```bash
git clone https://github.com/MatoTeziTanka/Family-Care-Ideas.git
cd Family-Care-Ideas
```

5. **Delete future1 (after admin validated):**
```bash
sudo deluser --remove-home future1
```

---

**Use Method 1 (copy/paste) - it's the fastest!** 🚀

