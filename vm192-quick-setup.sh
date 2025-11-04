#!/bin/bash

# VM192 (Personal) - Quick Setup Script
# Run as: sudo bash vm192-quick-setup.sh

set -e  # Exit on error

echo "========================================="
echo "VM192 (Personal) - Automated Setup"
echo "========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}Please run as root (sudo)${NC}"
    exit 1
fi

echo -e "${GREEN}Step 1: Updating system packages${NC}"
apt update && apt upgrade -y

echo -e "${GREEN}Step 2: Installing essential tools${NC}"
apt install -y \
    net-tools \
    curl \
    wget \
    git \
    nano \
    vim \
    htop \
    ufw \
    fail2ban \
    unattended-upgrades \
    docker.io \
    docker-compose

echo -e "${GREEN}Step 3: Setting hostname to 'personal'${NC}"
hostnamectl set-hostname personal

# Update /etc/hosts
if ! grep -q "personal" /etc/hosts; then
    echo "127.0.1.1       personal" >> /etc/hosts
    echo "192.168.12.192  personal" >> /etc/hosts
fi

echo -e "${GREEN}Step 4: Creating admin user${NC}"
if ! id "admin" &>/dev/null; then
    adduser --gecos "" admin
    usermod -aG sudo admin
    usermod -aG docker admin
    echo -e "${YELLOW}Admin user created. Set password manually!${NC}"
else
    echo "Admin user already exists"
fi

echo -e "${GREEN}Step 5: Configuring firewall${NC}"
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw allow 3000/tcp  # Frontend
ufw allow 8000/tcp  # Backend API
ufw --force enable

echo -e "${GREEN}Step 6: Configuring fail2ban${NC}"
systemctl enable fail2ban
systemctl start fail2ban

echo -e "${GREEN}Step 7: Enabling Docker${NC}"
systemctl enable docker
systemctl start docker

echo -e "${GREEN}Step 8: Configuring automatic security updates${NC}"
dpkg-reconfigure -plow unattended-upgrades

echo -e "${GREEN}Step 9: Cleaning up${NC}"
apt autoremove -y
apt clean

echo ""
echo "========================================="
echo -e "${GREEN}Setup Complete!${NC}"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Reboot the system: sudo reboot"
echo "2. SSH as admin: ssh admin@192.168.12.192"
echo "3. Configure static IP (see VM192-SETUP.md)"
echo "4. Delete future1 user after validation"
echo "5. Clone projects: git clone https://github.com/MatoTeziTanka/Family-Care-Ideas.git"
echo ""
echo "System Information:"
echo "  Hostname: $(hostname)"
echo "  IP: $(ip -4 addr show | grep inet | grep -v 127.0.0.1 | awk '{print $2}' | head -1)"
echo "  Docker: $(docker --version 2>/dev/null || echo 'Not available')"
echo "  UFW Status: $(ufw status | grep Status)"
echo ""
echo "🦅 Semper Fi!"

