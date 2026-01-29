# How to Get Reddit API Credentials

This guide will walk you through creating a Reddit app and obtaining your API credentials (client_id and client_secret).

## Prerequisites

- A Reddit account
- 5 minutes of your time

## Step-by-Step Instructions

### 1. Go to Reddit Apps Page

Visit: **https://www.reddit.com/prefs/apps**

(You must be logged in to Reddit)

### 2. Create a New App

Scroll to the bottom and click the button: **"are you a developer? create an app..."**

### 3. Fill in the Form

You'll see a form with these fields:

- **name**: `reddit_url_scraper`
  - This is just for your reference, can be anything

- **App type**: Select **"script"**
  - This is important! Choose the "script" radio button

- **description**: `URL scraper for extracting external links`
  - Optional, but helpful for your records

- **about url**: (leave blank)
  - Not needed for script apps

- **permissions**: (leave default)
  - Not needed for read-only access

- **redirect uri**: `http://localhost:8080`
  - Required field but not used for script apps
  - Just put any localhost URL

### 4. Create the App

Click the **"create app"** button at the bottom

### 5. Get Your Credentials

After creating, you'll see your app details:

```
reddit_url_scraper                             edit  delete
personal use script                            [client_id is here]

secret                                         [client_secret is here]
```

**Copy these two values**:

1. **client_id**: The string directly under "personal use script"
   - Example: `abc123XYZ789`
   - It's about 12-14 characters

2. **client_secret**: The string next to "secret"
   - Example: `xyz789ABC123def456GHI789`
   - It's about 27 characters

### 6. Configure Your Scraper

Edit `config.ini`:

```ini
[reddit]
client_id = abc123XYZ789
client_secret = xyz789ABC123def456GHI789
user_agent = linux:reddit_url_scraper:v1.0 (by /u/your_reddit_username)
```

**User Agent Format**:
- `platform:app_name:version (by /u/your_username)`
- Replace `your_reddit_username` with your actual Reddit username
- Examples:
  - `macos:reddit_url_scraper:v1.0 (by /u/john_doe)`
  - `windows:url_extractor:v1.0 (by /u/jane_smith)`

### 7. Test Your Setup

```bash
python reddit_url_scraper.py --backfill 7 --subreddits test
```

If you see `🔍 Scraping r/test...`, it's working!

## Visual Example

```
┌─────────────────────────────────────────┐
│ reddit_url_scraper                      │
│ personal use script    abc123XYZ789     │ ← This is your client_id
│                                         │
│ secret    xyz789ABC123def456GHI789      │ ← This is your client_secret
│                                         │
│ redirect uri    http://localhost:8080   │
│                                         │
│ [update app]  [delete]                  │
└─────────────────────────────────────────┘
```

## Troubleshooting

### "received 401 HTTP response"

Your credentials are incorrect. Double-check:
1. client_id is the string under "personal use script" (shorter one)
2. client_secret is the string next to "secret" (longer one)
3. No extra spaces or newlines when copying

### "Please replace placeholder value"

You forgot to edit `config.ini`. Make sure you:
1. Copied `config.ini.example` to `config.ini`
2. Replaced all the `YOUR_CLIENT_ID` placeholders with real values

### "Config file not found"

```bash
cp config.ini.example config.ini
nano config.ini  # Then add your credentials
```

### Can't find the apps page

Make sure you're logged in, then go directly to:
https://www.reddit.com/prefs/apps

### What if I lose my credentials?

Just go back to https://www.reddit.com/prefs/apps and you'll see your apps. The client_id is always visible. Click "edit" to see the secret again.

## Security Notes

⚠️ **Keep your credentials private**:
- Never commit `config.ini` to git (it's in `.gitignore`)
- Don't share your client_secret publicly
- If exposed, delete the app and create a new one

✅ **These credentials are read-only**:
- They can only read public Reddit data
- Cannot post, comment, or modify anything
- Cannot access private subreddits
- Safe to use for scraping

## API Limits

Reddit API is generous:
- ✅ **Free forever** (no credit card needed)
- ✅ **60 requests per minute**
- ✅ **No daily limit** for reasonable use
- ✅ **Perfect for daily scraping**

For this scraper:
- Backfill 90 days: ~1-5 requests per subreddit
- Daily mode: ~1 request per subreddit
- Well within limits! 🚀

## Need More Help?

1. Reddit API documentation: https://www.reddit.com/dev/api
2. PRAW documentation: https://praw.readthedocs.io
3. Reddit API support: r/redditdev

---

**That's it!** Once you have your `config.ini` set up, you're ready to scrape. 🎉
