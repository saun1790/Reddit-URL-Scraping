# Reddit URL Scraper

Professional tool to extract external URLs from Reddit subreddit posts. Includes interactive web dashboard and supports historical data backfill up to 6 months.

---

## Features

- ✅ **Backfill mode**: Extract posts from last N days (up to 180 days / 6 months)
- ✅ **Daily mode**: Fetch only new posts since last run
- ✅ **No duplicates**: SQLite database with unique constraints
- ✅ **Smart filtering**: Ignores Reddit internal links
- ✅ **Multiple subreddits**: Track unlimited subreddits simultaneously
- ✅ **CSV export**: Clean output with one click
- ✅ **Web dashboard**: Interactive UI with search, sort, and filters

---

## Requirements

- Python 3.8+
- Internet connection

---

## Installation

### 1. Install Dependencies

```bash
cd reddit_scraper
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. No API Keys Required

This scraper uses Reddit's public API without authentication.

---

## Usage

### Option 1: Web Dashboard (Recommended)

**Start the server:**

```bash
cd reddit_scraper
source venv/bin/activate
python web_viewer.py
```

**Open in browser:**

```
http://localhost:3010
```

**Dashboard Features:**

- View all URLs with search and filters
- Sort columns by clicking headers
- Resize columns by dragging edges
- Fetch URLs with real-time progress
- Export to CSV
- Configure subreddits

---

### Option 2: Command Line

**Initial backfill (6 months of data):**

```bash
python reddit_scraper_noauth.py --backfill 180 --subreddits SideProject
```

**Daily update (new posts only):**

```bash
python reddit_scraper_noauth.py --daily --subreddits SideProject
```

**Multiple subreddits:**

```bash
python reddit_scraper_noauth.py --backfill 90 --subreddits SideProject startups entrepreneur
```

**Export to CSV:**

```bash
python reddit_scraper_noauth.py --export output.csv
```

**Show statistics:**

```bash
python reddit_scraper_noauth.py --stats
```

---

## Data Structure

| Field | Description | Example |
|-------|-------------|---------|
| **url** | External URL found | https://example.com |
| **post_date** | Post timestamp | 2026-01-29 10:30:15 |
| **subreddit** | Source subreddit | SideProject |
| **post_id** | Unique post ID | 1qq7qfq |

**Database:** SQLite stored in `reddit_urls.db`

**CSV Export:** Standard format compatible with Excel/Google Sheets

---

## Automation

### macOS/Linux - Cron

```bash
crontab -e
```

Add this line (replace path):

```bash
0 9 * * * cd /path/to/reddit_scraper && ./venv/bin/python reddit_scraper_noauth.py --daily --subreddits SideProject
```

This runs the scraper daily at 9:00 AM.

### Windows - Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Action: Start a program
4. Program: `C:\path\to\venv\Scripts\python.exe`
5. Arguments: `reddit_scraper_noauth.py --daily --subreddits SideProject`
6. Start in: `C:\path\to\reddit_scraper`

---

## Capabilities

| Feature | Details |
|---------|---------|
| **Historical data** | Up to 6 months (~180 days) |
| **Concurrent subreddits** | Unlimited |
| **Deduplication** | Automatic via database constraints |
| **Rate limiting** | Built-in Reddit API compliance |
| **URL filtering** | Removes Reddit internal links |
| **Daily updates** | Incremental scraping |

---

## Project Structure

```
reddit_scraper/
├── reddit_scraper_noauth.py  # Main scraper
├── web_viewer.py              # Web dashboard
├── database.py                # SQLite handler
├── reddit_urls.db            # Database file
├── requirements.txt           # Python dependencies
├── templates/
│   └── index.html            # Dashboard frontend
└── README.md                 # Documentation
```

---

## Useful Commands

```bash
python reddit_scraper_noauth.py --stats

python reddit_scraper_noauth.py --export reddit_urls_$(date +%Y%m%d).csv

python reddit_scraper_noauth.py --backfill 90 --subreddits SideProject startups

python web_viewer.py
```

---

## License

MIT License - Free to use and modify.

---

## Quick Start

1. Install dependencies: `pip install -r requirements.txt`
2. Start dashboard: `python web_viewer.py`
3. Open browser: `http://localhost:3010`
4. Click "Fetch URLs" and select Backfill (90-180 days)
5. Done! URLs are stored in the database

**Recommendation:** Run a 90-180 day backfill first, then use daily mode to keep updated.
