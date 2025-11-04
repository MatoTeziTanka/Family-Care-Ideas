# 🔧 VM192 SSH Troubleshooting Guide

**Problem:** Cannot SSH into VM192 (192.168.12.192)  
**Access:** Web console available  
**User:** future1  
**Password:** Norelec7!

---

## 🎯 Quick Diagnostics (Run via Web Console)

Log into VM via web console (ESXi/Proxmox) and run these commands:

### Step 1: Verify Basic Connectivity

```bash
# Check IP address
ip addr show
# Should show 192.168.12.192

# Check if we can ping gateway
ping -c 3 192.168.12.1

# Check if we can ping another device
ping -c 3 192.168.12.180
```

### Step 2: Check SSH Service Status

```bash
# Check if SSH is running
sudo systemctl status sshd
# or
sudo systemctl status ssh

# If not running, start it
sudo systemctl start sshd
sudo systemctl enable sshd

# Check if SSH is listening on port 22
sudo netstat -tlnp | grep :22
# or
sudo ss -tlnp | grep :22
```

**Expected output:**
```
tcp   0   0 0.0.0.0:22   0.0.0.0:*   LISTEN   1234/sshd
```

### Step 3: Check Firewall

```bash
# Check if firewall is blocking SSH
sudo ufw status

# If UFW is active and blocking, allow SSH
sudo ufw allow 22/tcp
sudo ufw reload

# Or check iptables
sudo iptables -L -n | grep 22
```

### Step 4: Test SSH Locally

```bash
# Try SSH to localhost (from VM console)
ssh future1@localhost
# If this works, it's a network/firewall issue
# If this fails, it's an SSH configuration issue

# Also try:
ssh future1@192.168.12.192
```

### Step 5: Check SSH Configuration

```bash
# View SSH config
sudo cat /etc/ssh/sshd_config | grep -v "^#" | grep -v "^$"
```

**Look for these critical settings:**
```
Port 22
PermitRootLogin prohibit-password
PasswordAuthentication yes        # Should be yes
PubkeyAuthentication yes
```

### Step 6: Check Network Configuration

```bash
# Verify IP is set correctly
ip addr show | grep inet

# Check routing
ip route show

# Check DNS
cat /etc/resolv.conf

# Test connectivity from VM
ping 8.8.8.8
```

---

## 🔥 Common Fixes

### Fix 1: SSH Service Not Running

```bash
# Start SSH service
sudo systemctl start sshd
sudo systemctl enable sshd

# Verify it's running
sudo systemctl status sshd
```

### Fix 2: Firewall Blocking SSH

```bash
# Check firewall status
sudo ufw status

# If active, allow SSH
sudo ufw allow 22/tcp
sudo ufw reload

# Or temporarily disable to test
sudo ufw disable
# Try SSH now
# If it works, re-enable with SSH allowed:
sudo ufw enable
```

### Fix 3: SSH Config Issue - Password Auth Disabled

```bash
# Edit SSH config
sudo nano /etc/ssh/sshd_config
```

**Ensure these lines are set:**
```
PasswordAuthentication yes
PermitRootLogin prohibit-password
PubkeyAuthentication yes
UsePAM yes
```

**Restart SSH after changes:**
```bash
sudo systemctl restart sshd
```

### Fix 4: Wrong IP Address

```bash
# Check current IP
ip addr show

# If wrong, find network interface name
ip link show

# Edit netplan config (Ubuntu 18.04+)
sudo nano /etc/netplan/00-installer-config.yaml
```

**Example config:**
```yaml
network:
  version: 2
  ethernets:
    ens160:  # Your interface name
      addresses:
        - 192.168.12.192/24
      gateway4: 192.168.12.1
      nameservers:
        addresses:
          - 8.8.8.8
          - 1.1.1.1
```

**Apply:**
```bash
sudo netplan apply
```

### Fix 5: SELinux/AppArmor Blocking (Rare)

```bash
# Check if SELinux is enforcing
getenforce

# If enforcing, temporarily set to permissive
sudo setenforce 0

# Or check AppArmor
sudo aa-status
```

---

## 🧪 Complete SSH Reset

If nothing else works, reset SSH completely:

```bash
# Reinstall OpenSSH server
sudo apt update
sudo apt install --reinstall openssh-server -y

# Reset SSH config to defaults
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup
sudo rm /etc/ssh/sshd_config
sudo apt install --reinstall openssh-server -y

# Edit new config
sudo nano /etc/ssh/sshd_config
```

**Add these essential lines:**
```
Port 22
PasswordAuthentication yes
PubkeyAuthentication yes
PermitRootLogin prohibit-password
UsePAM yes
```

**Restart SSH:**
```bash
sudo systemctl restart sshd
sudo systemctl enable sshd
```

---

## 📡 Test from Your Main Machine (192.168.12.180)

Once you've fixed SSH on the VM, test from your main machine:

```bash
# Test connectivity
ping -c 3 192.168.12.192

# Test if SSH port is open
nc -zv 192.168.12.192 22
# or
telnet 192.168.12.192 22

# Try SSH
ssh future1@192.168.12.192
```

---

## 🔍 Advanced Diagnostics

### Check SSH Logs (on VM via console)

```bash
# View SSH logs
sudo tail -100 /var/log/auth.log | grep sshd
# or
sudo journalctl -u sshd -n 50

# Watch logs in real-time (in one terminal)
sudo tail -f /var/log/auth.log

# Then try SSH from another machine and watch for errors
```

### Check Network Connectivity

```bash
# From your main machine (192.168.12.180)
ping 192.168.12.192
traceroute 192.168.12.192
nmap -p 22 192.168.12.192

# Check if port 22 is open
nmap -sV -p 22 192.168.12.192
```

### Generate SSH Debug Output

```bash
# From your main machine, try SSH with verbose output
ssh -vvv future1@192.168.12.192
# This will show exactly where the connection fails
```

### Check Listening Services on VM

```bash
# See all listening ports
sudo netstat -tlnp
# or
sudo ss -tlnp

# Specifically check SSH
sudo lsof -i :22
```

---

## ✅ Verification Checklist

Run these on the VM (via console) and check results:

```bash
#!/bin/bash
echo "=== VM192 SSH Diagnostics ==="
echo ""
echo "1. IP Address:"
ip addr show | grep "inet 192.168.12.192" && echo "✅ IP is correct" || echo "❌ IP is wrong"
echo ""
echo "2. SSH Service:"
systemctl is-active sshd && echo "✅ SSH is running" || echo "❌ SSH is NOT running"
echo ""
echo "3. SSH Listening:"
ss -tlnp | grep :22 && echo "✅ SSH is listening on port 22" || echo "❌ SSH not listening"
echo ""
echo "4. Firewall Status:"
ufw status | grep "22/tcp.*ALLOW" && echo "✅ Firewall allows SSH" || echo "⚠️  Check firewall"
echo ""
echo "5. Gateway Reachable:"
ping -c 1 192.168.12.1 > /dev/null 2>&1 && echo "✅ Can reach gateway" || echo "❌ Cannot reach gateway"
echo ""
echo "6. SSH Config:"
grep "^PasswordAuthentication yes" /etc/ssh/sshd_config && echo "✅ Password auth enabled" || echo "❌ Password auth disabled"
echo ""
echo "7. Port 22 Open:"
netstat -tlnp | grep ":22 " && echo "✅ Port 22 open" || echo "❌ Port 22 not open"
```

Save as `ssh-check.sh` and run:
```bash
chmod +x ssh-check.sh
./ssh-check.sh
```

---

## 🚀 Most Likely Issues (In Order)

### 1. **Firewall Blocking** (90% of cases)
```bash
sudo ufw allow 22/tcp
sudo ufw reload
```

### 2. **SSH Service Not Running**
```bash
sudo systemctl start sshd
sudo systemctl enable sshd
```

### 3. **Wrong Network Configuration**
```bash
# Verify IP is set
ip addr show
# Verify gateway is reachable
ping 192.168.12.1
```

### 4. **Password Auth Disabled**
```bash
sudo nano /etc/ssh/sshd_config
# Set: PasswordAuthentication yes
sudo systemctl restart sshd
```

---

## 📞 Quick Fix Commands (Copy/Paste)

Run these all at once via web console:

```bash
# Quick SSH fix - run all at once
sudo systemctl start sshd
sudo systemctl enable sshd
sudo ufw allow 22/tcp
sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/g' /etc/ssh/sshd_config
sudo sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd_config
sudo systemctl restart sshd
echo "SSH should now work! Try: ssh future1@192.168.12.192"
```

---

## 🎯 Once SSH Works

After you can SSH successfully:

```bash
# Test from main machine
ssh future1@192.168.12.192

# If successful, run the setup script
curl -fsSL https://raw.githubusercontent.com/MatoTeziTanka/Family-Care-Ideas/main/vm192-quick-setup.sh -o setup.sh
sudo bash setup.sh
```

---

## 📋 Information to Share

If SSH still doesn't work, share these outputs (via web console):

```bash
# 1. IP configuration
ip addr show

# 2. SSH service status
sudo systemctl status sshd

# 3. Firewall status
sudo ufw status verbose

# 4. SSH listening status
sudo ss -tlnp | grep :22

# 5. SSH config
sudo grep "^PasswordAuthentication\|^Port\|^PermitRootLogin" /etc/ssh/sshd_config

# 6. Recent SSH logs
sudo journalctl -u sshd -n 20
```

---

**Start with the "Quick Fix Commands" above - they'll fix 95% of SSH issues!** 🚀

