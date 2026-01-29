#!/bin/bash
set -e

# ============================================
# Reddit URL Scraper - Production Installer
# Ubuntu/Debian VPS with nginx + SSL
# ============================================

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() { echo -e "${GREEN}[✓]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[!]${NC} $1"; }
print_error() { echo -e "${RED}[✗]${NC} $1"; }

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    print_error "Please run as root: sudo ./install-production.sh yourdomain.com"
    exit 1
fi

# Check domain argument
if [ -z "$1" ]; then
    print_error "Usage: sudo ./install-production.sh yourdomain.com [email]"
    print_warning "Example: sudo ./install-production.sh scraper.example.com admin@example.com"
    exit 1
fi

DOMAIN="$1"
EMAIL="${2:-admin@$DOMAIN}"
APP_DIR=$(pwd)
APP_USER=$(stat -c '%U' "$APP_DIR" 2>/dev/null || ls -ld "$APP_DIR" | awk '{print $3}')

echo ""
echo "============================================"
echo "🚀 Reddit URL Scraper - Production Setup"
echo "============================================"
echo "Domain: $DOMAIN"
echo "Email: $EMAIL"
echo "App Directory: $APP_DIR"
echo "App User: $APP_USER"
echo "============================================"
echo ""

read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi

# ============================================
# 1. Install dependencies
# ============================================
print_status "Installing system dependencies..."
apt update
apt install -y python3 python3-venv python3-pip nginx certbot python3-certbot-nginx ufw

# ============================================
# 2. Setup Python environment
# ============================================
print_status "Setting up Python environment..."
if [ ! -d "$APP_DIR/venv" ]; then
    python3 -m venv "$APP_DIR/venv"
fi
"$APP_DIR/venv/bin/pip" install --upgrade pip
"$APP_DIR/venv/bin/pip" install flask requests gunicorn

# ============================================
# 3. Create .env file for credentials
# ============================================
print_status "Creating environment configuration..."
if [ ! -f "$APP_DIR/.env" ]; then
    # Generate random password
    ADMIN_PASS=$(openssl rand -base64 12 | tr -dc 'a-zA-Z0-9' | head -c 16)
    SECRET_KEY=$(openssl rand -hex 32)
    
    cat > "$APP_DIR/.env" << ENVEOF
# Reddit Scraper Configuration
ADMIN_USERNAME=admin
ADMIN_PASSWORD=$ADMIN_PASS
SECRET_KEY=$SECRET_KEY
ENVEOF
    
    chown "$APP_USER:$APP_USER" "$APP_DIR/.env"
    chmod 600 "$APP_DIR/.env"
    
    print_status "Generated credentials saved to .env"
    echo ""
    echo "============================================"
    echo -e "${GREEN}🔐 LOGIN CREDENTIALS${NC}"
    echo "   Username: admin"
    echo "   Password: $ADMIN_PASS"
    echo "============================================"
    echo ""
else
    print_warning ".env already exists, skipping credential generation"
fi

# ============================================
# 4. Create systemd service
# ============================================
print_status "Creating systemd service..."
cat > /etc/systemd/system/reddit-scraper.service << SERVICEEOF
[Unit]
Description=Reddit URL Scraper Web Dashboard
After=network.target

[Service]
Type=simple
User=$APP_USER
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
EnvironmentFile=$APP_DIR/.env
ExecStart=$APP_DIR/venv/bin/gunicorn --workers 2 --bind 127.0.0.1:3010 web_viewer:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
SERVICEEOF

# ============================================
# 5. Create daily scraper timer
# ============================================
print_status "Creating daily scraper timer..."
cat > /etc/systemd/system/reddit-scraper-daily.service << DAILYEOF
[Unit]
Description=Reddit URL Scraper Daily Fetch
After=network.target

[Service]
Type=oneshot
User=$APP_USER
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/venv/bin/python reddit_scraper_noauth.py --daily --subreddits SideProject
DAILYEOF

cat > /etc/systemd/system/reddit-scraper-daily.timer << TIMEREOF
[Unit]
Description=Run Reddit Scraper Daily at 9 AM

[Timer]
OnCalendar=*-*-* 09:00:00
Persistent=true

[Install]
WantedBy=timers.target
TIMEREOF

# ============================================
# 6. Configure nginx
# ============================================
print_status "Configuring nginx..."
cat > /etc/nginx/sites-available/reddit-scraper << NGINXEOF
server {
    listen 80;
    server_name $DOMAIN;

    location / {
        proxy_pass http://127.0.0.1:3010;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_connect_timeout 60s;
        proxy_read_timeout 60s;
    }
}
NGINXEOF

# Enable site
ln -sf /etc/nginx/sites-available/reddit-scraper /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default 2>/dev/null || true

# Test nginx config
nginx -t

# ============================================
# 7. Configure firewall
# ============================================
print_status "Configuring firewall..."
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

# ============================================
# 8. Start services
# ============================================
print_status "Starting services..."
systemctl daemon-reload
systemctl enable reddit-scraper
systemctl start reddit-scraper
systemctl enable reddit-scraper-daily.timer
systemctl start reddit-scraper-daily.timer
systemctl restart nginx

# ============================================
# 9. Setup SSL with Let's Encrypt
# ============================================
print_status "Setting up SSL certificate..."
certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos -m "$EMAIL" --redirect

# ============================================
# Done!
# ============================================
echo ""
echo "============================================"
echo -e "${GREEN}✅ INSTALLATION COMPLETE!${NC}"
echo "============================================"
echo ""
echo "🌐 Your app is live at: https://$DOMAIN"
echo ""
echo "🔐 Login credentials are in: $APP_DIR/.env"
cat "$APP_DIR/.env" | grep -E "^ADMIN" | sed 's/^/   /'
echo ""
echo "📋 Useful commands:"
echo "   sudo systemctl status reddit-scraper    # Check status"
echo "   sudo systemctl restart reddit-scraper   # Restart app"
echo "   sudo journalctl -u reddit-scraper -f    # View logs"
echo "   sudo systemctl list-timers              # Check daily timer"
echo ""
echo "============================================"
