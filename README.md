# Reddit URL Scraper

Extract external URLs from Reddit subreddit posts. Includes web dashboard and historical backfill up to 6 months.

## Technologies

| Component | Technology | Description |
|-----------|------------|-------------|
| **Backend** | Python 3.8+ | Main programming language |
| **Web Framework** | Flask | Lightweight web server for dashboard |
| **Database** | SQLite | Local database, no server required |
| **Reddit Data** | Reddit Public API | No authentication required, uses JSON endpoints |
| **Frontend** | HTML5 / CSS3 / JavaScript | Single-page dashboard with vanilla JS |
| **HTTP Client** | Requests | Python library for API calls |

## Features

- Backfill mode: Extract posts from last N days (up to 180 days)
- Daily mode: Fetch only new posts since last run
- No duplicates: SQLite database with unique constraints
- Multiple subreddits: Track unlimited subreddits
- CSV export: One click download
- Web dashboard: Interactive UI with search and filters

## Prerequisites

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip git -y
python3 --version
```

### Linux (CentOS/RHEL/Fedora)

```bash
sudo dnf install python3 python3-pip git -y
python3 --version
```

### macOS

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python and Git
brew install python git
python3 --version
```

### Windows

1. **Install Python:**
   - Download from https://www.python.org/downloads/
   - Run installer
   - **IMPORTANT:** Check "Add Python to PATH" during installation
   - Click "Install Now"

2. **Install Git:**
   - Download from https://git-scm.com/download/win
   - Run installer with default options

3. **Verify installation (PowerShell):**
   ```powershell
   python --version
   git --version
   ```

## Installation

### Linux / macOS

```bash
mkdir ~/projects
cd ~/projects
git clone https://github.com/saun1790/Reddit-URL-Scraping.git
cd Reddit-URL-Scraping
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
```

### Windows (PowerShell)

```powershell
mkdir C:\projects
cd C:\projects
git clone https://github.com/saun1790/Reddit-URL-Scraping.git
cd Reddit-URL-Scraping
python -m venv venv
.\venv\Scripts\pip install -r requirements.txt
```

## Web Dashboard

### Linux / macOS

**Start (foreground):**
```bash
cd ~/projects/Reddit-URL-Scraping
./venv/bin/python web_viewer.py
```

**Start (background):**
```bash
cd ~/projects/Reddit-URL-Scraping
nohup ./venv/bin/python web_viewer.py > web_viewer.log 2>&1 &
echo $! > web_viewer.pid
```

**Stop:**
```bash
cd ~/projects/Reddit-URL-Scraping
kill $(cat web_viewer.pid)
```

**Restart:**
```bash
cd ~/projects/Reddit-URL-Scraping
kill $(cat web_viewer.pid) 2>/dev/null
nohup ./venv/bin/python web_viewer.py > web_viewer.log 2>&1 &
echo $! > web_viewer.pid
```

**View logs:**
```bash
tail -f web_viewer.log
```

### Windows

**Start (foreground):**
```powershell
cd C:\projects\Reddit-URL-Scraping
.\venv\Scripts\python web_viewer.py
```

**Start (background):**
```powershell
cd C:\projects\Reddit-URL-Scraping
Start-Process -WindowStyle Hidden -FilePath ".\venv\Scripts\python.exe" -ArgumentList "web_viewer.py" -RedirectStandardOutput "web_viewer.log" -RedirectStandardError "web_viewer_error.log"
```

**Stop:**
```powershell
Get-Process python | Stop-Process
```

**Open in browser:**
```
http://localhost:3010
```

## Command Line

### Linux / macOS

**Backfill 6 months:**
```bash
cd ~/projects/Reddit-URL-Scraping
./venv/bin/python reddit_scraper_noauth.py --backfill 180 --subreddits SideProject
```

**Daily update:**
```bash
cd ~/projects/Reddit-URL-Scraping
./venv/bin/python reddit_scraper_noauth.py --daily --subreddits SideProject
```

**Multiple subreddits:**
```bash
./venv/bin/python reddit_scraper_noauth.py --backfill 90 --subreddits SideProject startups entrepreneur
```

**Export CSV:**
```bash
./venv/bin/python reddit_scraper_noauth.py --export output.csv
```

**Statistics:**
```bash
./venv/bin/python reddit_scraper_noauth.py --stats
```

### Windows

**Backfill 6 months:**
```powershell
cd C:\projects\Reddit-URL-Scraping
.\venv\Scripts\python reddit_scraper_noauth.py --backfill 180 --subreddits SideProject
```

**Daily update:**
```powershell
.\venv\Scripts\python reddit_scraper_noauth.py --daily --subreddits SideProject
```

## Automation (Cron)

### Linux / macOS

```bash
crontab -e
```

Add:
```bash
0 9 * * * cd ~/projects/Reddit-URL-Scraping && ./venv/bin/python reddit_scraper_noauth.py --daily --subreddits SideProject >> cron.log 2>&1
```

## Data Structure

| Field | Description |
|-------|-------------|
| url | External URL found |
| post_date | Post timestamp |
| subreddit | Source subreddit |
| post_id | Reddit post ID |

Database: `reddit_urls.db` (SQLite)

## Project Structure

```
Reddit-URL-Scraping/
├── web_viewer.py             # Web dashboard
├── reddit_scraper_noauth.py  # Main scraper
├── database.py               # SQLite handler
├── reddit_urls.db            # Database
├── requirements.txt          # Dependencies
└── templates/
    └── index.html            # Dashboard UI
```

## License

MIT
