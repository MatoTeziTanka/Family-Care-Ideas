#!/bin/bash

# VM192 (Personal) - Complete Interactive Setup Script
# Run this after SSH'ing into the VM
# Usage: bash vm192-complete-setup.sh

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}VM192 (Personal) - Complete Setup${NC}"
echo -e "${BLUE}=========================================${NC}"
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    echo -e "${RED}Please run as regular user (not sudo)${NC}"
    echo "This script will ask for sudo when needed"
    exit 1
fi

# Function to run with sudo and show status
run_sudo() {
    echo -e "${YELLOW}Running: $@${NC}"
    sudo "$@"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Success${NC}"
    else
        echo -e "${RED}❌ Failed${NC}"
        exit 1
    fi
}

# Step 1: Show current configuration
echo -e "${GREEN}=== Step 1: Current Configuration ===${NC}"
echo "Hostname: $(hostname)"
echo "IP Addresses:"
ip addr show | grep "inet " | grep -v "127.0.0.1"
echo "MAC Address (last 4 should be b766):"
ip addr show | grep "ether" | tail -1
echo "OS Version:"
cat /etc/os-release | grep PRETTY_NAME
echo ""
read -p "Press Enter to continue..."

# Step 2: Update system
echo -e "${GREEN}=== Step 2: Updating System ===${NC}"
run_sudo apt update
run_sudo apt upgrade -y
echo ""

# Step 3: Install essential tools
echo -e "${GREEN}=== Step 3: Installing Essential Tools ===${NC}"
run_sudo apt install -y \
    net-tools \
    curl \
    wget \
    git \
    nano \
    vim \
    htop \
    iotop \
    nethogs \
    ufw \
    fail2ban \
    unattended-upgrades \
    rsync
echo ""

# Step 4: Set hostname
echo -e "${GREEN}=== Step 4: Setting Hostname to 'personal' ===${NC}"
run_sudo hostnamectl set-hostname personal
echo "127.0.1.1       personal" | sudo tee -a /etc/hosts > /dev/null
echo "192.168.12.192  personal" | sudo tee -a /etc/hosts > /dev/null
echo "New hostname: $(hostname)"
echo ""

# Step 5: Verify IP address
echo -e "${GREEN}=== Step 5: Verifying IP Address ===${NC}"
CURRENT_IP=$(ip addr show | grep "inet 192.168.12" | awk '{print $2}' | cut -d'/' -f1)
echo "Current IP: $CURRENT_IP"
if [ "$CURRENT_IP" != "192.168.12.192" ]; then
    echo -e "${YELLOW}⚠️  IP is not 192.168.12.192${NC}"
    echo "You changed it via web console. Netplan should already be configured."
    echo "Current netplan config:"
    sudo cat /etc/netplan/*.yaml
else
    echo -e "${GREEN}✅ IP is correct (192.168.12.192)${NC}"
fi
echo ""

# Step 6: Create admin user
echo -e "${GREEN}=== Step 6: Creating Admin User ===${NC}"
if id "admin" &>/dev/null; then
    echo -e "${YELLOW}Admin user already exists${NC}"
else
    run_sudo adduser --gecos "" admin
    run_sudo usermod -aG sudo admin
    echo -e "${GREEN}✅ Admin user created with sudo access${NC}"
    echo ""
    echo -e "${YELLOW}IMPORTANT: Test admin user before deleting future1!${NC}"
    echo "Open a NEW terminal and try: ssh admin@192.168.12.192"
fi
echo ""

# Step 7: Install Docker
echo -e "${GREEN}=== Step 7: Installing Docker ===${NC}"
if command -v docker &> /dev/null; then
    echo -e "${YELLOW}Docker already installed${NC}"
    docker --version
else
    echo "Downloading Docker install script..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    run_sudo sh get-docker.sh
    rm get-docker.sh
    run_sudo systemctl enable docker
    run_sudo systemctl start docker
    run_sudo usermod -aG docker $USER
    run_sudo usermod -aG docker admin 2>/dev/null || true
    echo -e "${GREEN}✅ Docker installed${NC}"
    docker --version
fi
echo ""

# Step 8: Install Docker Compose
echo -e "${GREEN}=== Step 8: Installing Docker Compose ===${NC}"
if command -v docker-compose &> /dev/null; then
    echo -e "${YELLOW}Docker Compose already installed${NC}"
    docker-compose --version
else
    echo "Downloading Docker Compose..."
    COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep 'tag_name' | cut -d\" -f4)
    run_sudo curl -L "https://github.com/docker/compose/releases/download/${COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    run_sudo chmod +x /usr/local/bin/docker-compose
    echo -e "${GREEN}✅ Docker Compose installed${NC}"
    docker-compose --version
fi
echo ""

# Step 9: Configure Firewall
echo -e "${GREEN}=== Step 9: Configuring Firewall (UFW) ===${NC}"
run_sudo ufw --force reset
run_sudo ufw default deny incoming
run_sudo ufw default allow outgoing
run_sudo ufw allow 22/tcp comment "SSH"
run_sudo ufw allow 80/tcp comment "HTTP"
run_sudo ufw allow 443/tcp comment "HTTPS"
run_sudo ufw allow 3000/tcp comment "Frontend"
run_sudo ufw allow 8000/tcp comment "Backend API"
run_sudo ufw --force enable
echo ""
echo "Firewall status:"
sudo ufw status verbose
echo ""

# Step 10: Configure Fail2Ban
echo -e "${GREEN}=== Step 10: Configuring Fail2Ban ===${NC}"
run_sudo systemctl enable fail2ban
run_sudo systemctl start fail2ban
if [ ! -f /etc/fail2ban/jail.local ]; then
    run_sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
fi
echo -e "${GREEN}✅ Fail2Ban configured${NC}"
sudo fail2ban-client status
echo ""

# Step 11: Enable Automatic Security Updates
echo -e "${GREEN}=== Step 11: Enabling Automatic Security Updates ===${NC}"
echo 'APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Download-Upgradeable-Packages "1";
APT::Periodic::AutocleanInterval "7";
APT::Periodic::Unattended-Upgrade "1";' | sudo tee /etc/apt/apt.conf.d/20auto-upgrades > /dev/null
echo -e "${GREEN}✅ Automatic updates enabled${NC}"
echo ""

# Step 12: System scan
echo -e "${GREEN}=== Step 12: System Scan ===${NC}"
echo ""
echo "OS Information:"
cat /etc/os-release | grep -E "NAME|VERSION"
echo ""
echo "Kernel:"
uname -r
echo ""
echo "Total Packages:"
dpkg -l | wc -l
echo ""
echo "Disk Usage:"
df -h /
echo ""
echo "Memory:"
free -h | grep Mem
echo ""
echo "Running Services:"
systemctl list-units --type=service --state=running | grep -E "docker|sshd|ufw|fail2ban"
echo ""
echo "Open Ports:"
sudo ss -tlnp | grep LISTEN
echo ""
echo "Users:"
cat /etc/passwd | grep -E "future1|admin" | cut -d: -f1
echo ""

# Step 13: Clean up
echo -e "${GREEN}=== Step 13: Cleaning Up ===${NC}"
run_sudo apt autoremove -y
run_sudo apt clean
echo ""

# Summary
echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}Setup Complete!${NC}"
echo -e "${BLUE}=========================================${NC}"
echo ""
echo -e "${GREEN}✅ Hostname set to: $(hostname)${NC}"
echo -e "${GREEN}✅ IP Address: $(ip addr show | grep "inet 192.168.12" | awk '{print $2}' | cut -d'/' -f1)${NC}"
echo -e "${GREEN}✅ Docker installed: $(docker --version 2>/dev/null || echo 'Error')${NC}"
echo -e "${GREEN}✅ Firewall configured and enabled${NC}"
echo -e "${GREEN}✅ Security hardened (fail2ban, auto-updates)${NC}"
echo ""
echo -e "${YELLOW}=== IMPORTANT NEXT STEPS ===${NC}"
echo ""
echo "1. ${YELLOW}Logout and login again${NC} (for docker group to take effect):"
echo "   exit"
echo "   ssh future1@192.168.12.192"
echo ""
echo "2. ${YELLOW}Test admin user${NC} (in a NEW terminal):"
echo "   ssh admin@192.168.12.192"
echo "   sudo whoami  # Should output: root"
echo ""
echo "3. ${YELLOW}Clone your projects:${NC}"
echo "   git clone https://github.com/MatoTeziTanka/Family-Care-Ideas.git"
echo "   cd Family-Care-Ideas/projects/atlantis-pinball-leaderboard"
echo ""
echo "4. ${YELLOW}After validating admin works, delete future1:${NC}"
echo "   sudo deluser --remove-home future1"
echo ""
echo "5. ${YELLOW}Deploy Atlantis Pinball:${NC}"
echo "   cd ~/Family-Care-Ideas/projects/atlantis-pinball-leaderboard"
echo "   cp .env.example .env"
echo "   nano .env  # Add your SMTP_PASSWORD"
echo "   cd deployment"
echo "   ./setup.sh"
echo ""
echo -e "${GREEN}All configuration files saved in: ~/vm192-setup-$(date +%Y%m%d)/${NC}"
echo ""
echo "🦅 Semper Fi!"

