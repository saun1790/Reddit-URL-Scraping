#!/bin/bash
# Daily Reddit URL Scraper - Cron Script
# Add to crontab: 0 8 * * * /path/to/run_daily.sh

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$SCRIPT_DIR/logs"
LOG_FILE="$LOG_DIR/scraper_$(date +%Y%m%d).log"
SUBREDDITS="SideProject startups entrepreneur"

# Create log directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Log start time
echo "========================================" >> "$LOG_FILE"
echo "Reddit URL Scraper - $(date)" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

# Change to script directory
cd "$SCRIPT_DIR" || exit 1

# Run the scraper
python3 reddit_url_scraper.py --daily --subreddits $SUBREDDITS >> "$LOG_FILE" 2>&1
EXIT_CODE=$?

# Log result
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Success - $(date)" >> "$LOG_FILE"
else
    echo "❌ Failed with exit code $EXIT_CODE - $(date)" >> "$LOG_FILE"
fi

echo "" >> "$LOG_FILE"

# Optional: Export CSV after successful run
if [ $EXIT_CODE -eq 0 ]; then
    python3 reddit_url_scraper.py --export "exports/reddit_urls_$(date +%Y%m%d).csv" >> "$LOG_FILE" 2>&1
fi

# Keep only last 30 days of logs
find "$LOG_DIR" -name "scraper_*.log" -mtime +30 -delete

exit $EXIT_CODE
