# Reddit URL Scraper

Extract external URLs from Reddit subreddit posts. Includes web dashboard and historical backfill up to 6 months.

![Dashboard Preview](https://img.shields.io/badge/Dashboard-Live-green) ![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue)

## Features

- 🔄 **Backfill mode**: Extract posts from last N days (up to 180 days)
- 📅 **Daily mode**: Fetch only new posts since last run
- 🚫 **No duplicates**: SQLite database with unique constraints
- 📊 **Multiple subreddits**: Track unlimited subreddits
- 📥 **CSV export**: One click download
- 🖥️ **Web dashboard**: Interactive UI with search, filters, and pagination
- 🔓 **No API keys required**: Uses Reddit's public JSON endpoints

## Technologies

| Component | Technology |
|-----------|------------|
| Backend | Python 3.8+ |
| Web Framework | Flask |
| Database | SQLite |
| Reddit Data | Public JSON API (no auth) |
| Frontend | HTML5 / CSS3 / Vanilla JS |

## Prerequisites

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip git -y
```

### Linux (CentOS/RHEL/Fedora)
```bash
sudo dnf install python3 python3-pip git -y
```

### macOS
```bash
brew install python git
```

### Windows
1. Download Python from https://www.python.org/downloads/
2. **IMPORTANT:** Check "Add Python to PATH" during installation
3. Download Git from https://git-scm.com/download/win

## Installation

### Linux / macOS
```bash
git clone https://github.com/saun1790/Reddit-URL-Scraping.git
cd Reddit-URL-Scraping
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
```

### Windows (PowerShell)
```powershell
git clone https://github.com/saun1790/Reddit-URL-Scraping.git
cd Reddit-URL-Scraping
python -m venv venv
.\venv\Scripts\pip install -r requirements.txt
```

## Quick Start

### Start the Web Dashboard

**Linux / macOS:**
```bash
./venv/bin/python web_viewer.py
```

**Windows:**
```powershell
.\venv\Scripts\python web_viewer.py
```

Open your browser: **http://localhost:3010**

### Dashboard Features

1. **⚙️ Settings** - Configure which subreddits to track (comma-separated, without r/)
2. **⚡ Fetch URLs** - Run scraper in Daily or Backfill mode
3. **🔍 Search** - Filter URLs by keyword
4. **📥 Export CSV** - Download all data

## Command Line Usage

### Backfill (Historical Data)
```bash
# Last 30 days
./venv/bin/python reddit_scraper_noauth.py --backfill 30 --subreddits SideProject

# Last 6 months, multiple subreddits
./venv/bin/python reddit_scraper_noauth.py --backfill 180 --subreddits SideProject startups entrepreneur
```

### Daily Update
```bash
./venv/bin/python reddit_scraper_noauth.py --daily --subreddits SideProject
```

### Export to CSV
```bash
./venv/bin/python reddit_scraper_noauth.py --export urls.csv
```

### View Statistics
```bash
./venv/bin/python reddit_scraper_noauth.py --stats
```

## Running in Background

### Linux / macOS
```bash
# Start
nohup ./venv/bin/python web_viewer.py > web_viewer.log 2>&1 &
echo $! > web_viewer.pid

# Stop
kill $(cat web_viewer.pid)

# View logs
tail -f web_viewer.log
```

### Windows (PowerShell)
```powershell
# Start
Start-Process -WindowStyle Hidden -FilePath ".\venv\Scripts\python.exe" -ArgumentList "web_viewer.py"

# Stop
Get-Process python | Stop-Process
```

## Automation (Cron)

Run daily at 9 AM:
```bash
crontab -e
```

Add:
```bash
0 9 * * * cd /path/to/Reddit-URL-Scraping && ./venv/bin/python reddit_scraper_noauth.py --daily --subreddits SideProject >> cron.log 2>&1
```

## Data Structure

| Field | Description |
|-------|-------------|
| `url` | External URL found in post |
| `post_date` | Post timestamp (UTC) |
| `subreddit` | Source subreddit |
| `post_id` | Reddit post ID |

Database file: `reddit_urls.db` (SQLite, created on first run)

## Project Structure

```
Reddit-URL-Scraping/
├── web_viewer.py             # Web dashboard server
├── reddit_scraper_noauth.py  # Main scraper (CLI)
├── database.py               # SQLite database handler
├── requirements.txt          # Python dependencies
├── templates/
│   └── index.html            # Dashboard UI
└── reddit_urls.db            # Database (auto-created)
```

## Troubleshooting

**Port 3010 already in use:**
```bash
# Find and kill process
lsof -i :3010
kill -9 <PID>
```

**Permission denied:**
```bash
chmod +x ./venv/bin/python
```

**Module not found:**
```bash
./venv/bin/pip install -r requirements.txt
```

## License

MIT

## Linux Service (systemd)

Create a systemd service to run the web dashboard automatically on boot.

### 1. Create Service File

```bash
sudo nano /etc/systemd/system/reddit-scraper.service
```

Paste the following (adjust paths and user):

```ini
[Unit]
Description=Reddit URL Scraper Web Dashboard
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/Reddit-URL-Scraping
ExecStart=/home/YOUR_USERNAME/Reddit-URL-Scraping/venv/bin/python web_viewer.py
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

> **Note:** Replace `YOUR_USERNAME` with your actual username and adjust paths if needed.

### 2. Enable and Start

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable on boot
sudo systemctl enable reddit-scraper

# Start service
sudo systemctl start reddit-scraper
```

### 3. Service Commands

| Command | Description |
|---------|-------------|
| `sudo systemctl start reddit-scraper` | Start the service |
| `sudo systemctl stop reddit-scraper` | Stop the service |
| `sudo systemctl restart reddit-scraper` | Restart the service |
| `sudo systemctl status reddit-scraper` | Check status |
| `sudo journalctl -u reddit-scraper -f` | View live logs |
| `sudo journalctl -u reddit-scraper --since today` | Today's logs |

### 4. Optional: Daily Scraper Service (Timer)

Create a timer to run the scraper daily:

```bash
sudo nano /etc/systemd/system/reddit-scraper-daily.service
```

```ini
[Unit]
Description=Reddit URL Scraper Daily Fetch
After=network.target

[Service]
Type=oneshot
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/Reddit-URL-Scraping
ExecStart=/home/YOUR_USERNAME/Reddit-URL-Scraping/venv/bin/python reddit_scraper_noauth.py --daily --subreddits SideProject
```

Create the timer:

```bash
sudo nano /etc/systemd/system/reddit-scraper-daily.timer
```

```ini
[Unit]
Description=Run Reddit Scraper Daily at 9 AM

[Timer]
OnCalendar=*-*-* 09:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

Enable the timer:

```bash
sudo systemctl daemon-reload
sudo systemctl enable reddit-scraper-daily.timer
sudo systemctl start reddit-scraper-daily.timer

# Check timer status
systemctl list-timers | grep reddit
```

### Quick Setup Script

Save this as `install-service.sh` and run with `sudo`:

```bash
#!/bin/bash
set -e

# Configuration
USER=$(whoami)
APP_DIR=$(pwd)

echo "📦 Installing Reddit Scraper service..."
echo "   User: $USER"
echo "   Directory: $APP_DIR"

# Create web dashboard service
cat > /etc/systemd/system/reddit-scraper.service << SERVICEEOF
[Unit]
Description=Reddit URL Scraper Web Dashboard
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/venv/bin/python web_viewer.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
SERVICEEOF

# Reload and enable
systemctl daemon-reload
systemctl enable reddit-scraper
systemctl start reddit-scraper

echo "✅ Service installed!"
echo ""
echo "Commands:"
echo "  sudo systemctl status reddit-scraper"
echo "  sudo systemctl restart reddit-scraper"
echo "  sudo journalctl -u reddit-scraper -f"
```

Run:
```bash
chmod +x install-service.sh
sudo ./install-service.sh
```

## Production Deployment (VPS with nginx + SSL)

One-command installation for Ubuntu/Debian VPS with nginx and Let's Encrypt SSL.

### Prerequisites

- Ubuntu 20.04+ or Debian 11+ VPS
- Domain pointing to your VPS IP
- Root access (sudo)

### Quick Install

```bash
# Clone repository
git clone https://github.com/saun1790/Reddit-URL-Scraping.git
cd Reddit-URL-Scraping

# Run production installer
sudo ./install-production.sh yourdomain.com your-email@example.com
```

### What the installer does:

1. ✅ Installs Python, nginx, certbot, ufw
2. ✅ Creates Python virtual environment
3. ✅ Generates secure admin credentials (saved to `.env`)
4. ✅ Configures systemd service (auto-start on boot)
5. ✅ Configures daily scraper timer (9 AM)
6. ✅ Sets up nginx as reverse proxy
7. ✅ Obtains SSL certificate from Let's Encrypt
8. ✅ Configures firewall (ports 22, 80, 443)

### After Installation

Your app will be live at `https://yourdomain.com`

**View credentials:**
```bash
cat .env
```

**Service commands:**
```bash
sudo systemctl status reddit-scraper      # Check status
sudo systemctl restart reddit-scraper     # Restart
sudo systemctl stop reddit-scraper        # Stop
sudo journalctl -u reddit-scraper -f      # Live logs
```

**SSL certificate renewal (automatic, but to test):**
```bash
sudo certbot renew --dry-run
```

### Manual nginx Configuration

If you prefer manual setup:

```nginx
# /etc/nginx/sites-available/reddit-scraper
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:3010;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Then run:
```bash
sudo ln -s /etc/nginx/sites-available/reddit-scraper /etc/nginx/sites-enabled/
sudo certbot --nginx -d yourdomain.com
sudo systemctl restart nginx
```

### Environment Variables

The app supports these environment variables (via `.env` file):

| Variable | Default | Description |
|----------|---------|-------------|
| `ADMIN_USERNAME` | admin | Login username |
| `ADMIN_PASSWORD` | (generated) | Login password |
| `SECRET_KEY` | (generated) | Flask session key |
| `DEBUG` | true | Debug mode (false in production) |

### Security Notes

- `.env` file has `chmod 600` (only owner can read)
- nginx proxies to localhost only (3010 not exposed)
- Firewall blocks all ports except 22, 80, 443
- SSL auto-renews via certbot timer
