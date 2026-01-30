# Reddit URL Scraper - User Manual

System to extract and organize URLs shared in Reddit subreddits.

## 🎯 What does it do?

Automatically collects **all URLs** (web links) from posts in the subreddits you configure:
- Projects, startups, tools
- Apps, websites, demos
- Everything is saved in a database
- Web dashboard to view and search easily

## ✨ Features

- 📊 **Visual Dashboard** - Easy-to-use web interface
- 🔍 **Search** - Find URLs by keyword
- 📥 **Export to Excel** - Download data as CSV
- 🔄 **Daily Updates** - Only gets new posts
- 📚 **Complete History** - Can fetch posts up to 6 months old
- 🚫 **No Duplicates** - Doesn't save the same URL twice
- 🔓 **No Reddit Account** - No login required

## 📋 Prerequisites (Windows)

1. **Python 3.8 or higher**
   - Download from: https://www.python.org/downloads/
   - ⚠️ **IMPORTANT:** Check "Add Python to PATH" during installation

2. **Git** (optional, for updates)
   - Download from: https://git-scm.com/download/win

---

## 🚀 Installation on Windows

### Step 1: Download the Project

**Option A - With Git:**
```powershell
git clone https://github.com/saun1790/Reddit-URL-Scraping.git
cd Reddit-URL-Scraping
```

**Option B - Without Git:**
1. Go to: https://github.com/saun1790/Reddit-URL-Scraping
2. Click green "Code" button → "Download ZIP"
3. Extract the file
4. Open PowerShell in that folder (Shift + Right-click → "Open PowerShell here")

### Step 2: Install Dependencies

```powershell
# If you get permission error, run this first:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Create virtual environment
python -m venv venv

# Install libraries
.\venv\Scripts\pip install -r requirements.txt
```

✅ **Installation complete!**

---

## 🖥️ Using the Dashboard

### Start the System

```powershell
.\venv\Scripts\python web_viewer.py
```

You'll see something like:
```
 * Running on http://127.0.0.1:3010
```

Open your browser at: **http://localhost:3010**

### Configure Subreddits

1. Click **⚙️ Settings** (top right corner)
2. Type the subreddit name **without** "r/" (example: `SideProject`)
3. Press Enter or click "+"
4. To remove: click ❌ next to the name

**Recommended subreddits:**
- `SideProject` - Personal projects
- `startups` - Startups and entrepreneurship  
- `entrepreneur` - Business
- `InternetIsBeautiful` - Interesting websites

### Fetch URLs

1. Click **⚡ Fetch URLs**
2. Select mode:
   - **Daily** (fast, 1-2 min) - Only new posts
   - **Backfill** (slow, 5-10 min) - Historical posts
3. Click **Start**
4. Wait for completion

### Search and Filter

- **Search:** Type keyword (e.g., "AI", "SaaS")
- **Filter:** Dropdown to view only one subreddit
- **Export:** "📥 Export CSV" button downloads everything to Excel

---

## 💻 Command Line Usage

### Daily Update (Recommended)

```powershell
.\venv\Scripts\python reddit_scraper_noauth.py --daily --subreddits SideProject startups
```

### Get Historical Data (First Time)

```powershell
# Last 30 days
.\venv\Scripts\python reddit_scraper_noauth.py --backfill 30 --subreddits SideProject

# Last 6 months
.\venv\Scripts\python reddit_scraper_noauth.py --backfill 180 --subreddits SideProject startups
```

### Export to CSV

```powershell
.\venv\Scripts\python reddit_scraper_noauth.py --export urls.csv
```

### View Statistics

```powershell
.\venv\Scripts\python reddit_scraper_noauth.py --stats
```

---

## 🔄 Update the System

If a new version is available:

```powershell
# With Git
git pull

# Reinstall dependencies (if there were changes)
.\venv\Scripts\pip install -r requirements.txt --upgrade
```

---

## 📊 Data Structure

Data is saved in `reddit_urls.db` (SQLite database)

| Field | Description |
|-------|-------------|
| `url` | Web link found in post |
| `post_date` | Post date (UTC) |
| `subreddit` | Which subreddit it comes from |
| `post_id` | Reddit post ID |

---

## 🆘 Troubleshooting

### "Port 3010 already in use"

Means you already have the dashboard open. Close the previous window or:

```powershell
# See what's using the port
netstat -ano | findstr :3010

# Kill the process (replace PID with the number that appears)
taskkill /PID <number> /F
```

### "ModuleNotFoundError: No module named 'flask'"

Reinstall dependencies:

```powershell
.\venv\Scripts\pip install -r requirements.txt
```

### "Permission error when activating venv"

Run this first:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Scraping very slow

- Use **Daily** instead of **Backfill**
- Reduce the number of days in Backfill
- Check your internet connection

### Not finding new URLs

Possible causes:
- No new posts in that subreddit
- You already have all recent posts
- The subreddit is inactive

**Solution:** Try another more active subreddit

---

## 📁 Project Files

```
Reddit-URL-Scraping/
├── web_viewer.py             # Web dashboard
├── reddit_scraper_noauth.py  # Scraper (command line)
├── database.py               # Database management
├── requirements.txt          # Required libraries
├── USER_GUIDE.md            # Complete user guide (NON-TECHNICAL)
├── templates/
│   └── index.html           # Dashboard interface
└── reddit_urls.db           # Database (created automatically)
```

---

## ❓ Frequently Asked Questions

**Do I need a Reddit account?**  
No, the system works without authentication.

**How many subreddits can I add?**  
As many as you want, but we recommend 3-5 to start.

**Is the data saved permanently?**  
Yes, everything is saved in `reddit_urls.db`. It's not lost when you close.

**Can I use this on another computer?**  
Yes, copy the entire folder (includes the `.db` file).

**How often should I run the scraper?**  
Depends on your needs:
- Daily if you want to stay up to date
- Weekly if you only check periodically
- Whenever you need it

---

## 📚 Additional Documentation

- **USER_GUIDE.md** - Complete user guide (recommended)
- **SUPER_SCRAPING_AGENT_PROMPT.md** - Advanced technical documentation

---

## 📞 Support

If you have problems:
1. Check this guide first
2. Consult **USER_GUIDE.md** for more details
3. Verify you have the latest version (`git pull`)

---

**Last updated:** January 2026  
**Version:** 1.0  
**License:** MIT
