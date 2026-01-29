#!/usr/bin/env python3

import requests
import re
import time
from datetime import datetime, timedelta, timezone
from typing import List, Set, Dict
import argparse
import sys
from database import Database

class RedditURLScraperNoAuth:
    
    
    URL_PATTERN = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    )
    
    REDDIT_DOMAINS = {
        'reddit.com', 'www.reddit.com', 'old.reddit.com', 'new.reddit.com',
        'redd.it', 'i.redd.it', 'v.redd.it', 'reddit.app.link', 'preview.redd.it'
    }
    
    ENDPOINTS = [
        ('new', {}),
        ('top', {'t': 'day'}),
        ('top', {'t': 'week'}),
        ('top', {'t': 'month'}),
        ('top', {'t': 'year'}),
        ('hot', {}),
        ('rising', {}),
    ]
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        self.db = Database()
    
    def extract_urls_from_text(self, text: str) -> Set[str]:
        
        if not text:
            return set()
        
        urls = self.URL_PATTERN.findall(text)
        normalized = set()
        
        for url in urls:
            url = url.rstrip('.,;:!?)]\'"')
            if not self._is_reddit_url(url):
                normalized.add(url)
        
        return normalized
    
    def _is_reddit_url(self, url: str) -> bool:
        
        url_lower = url.lower()
        return any(domain in url_lower for domain in self.REDDIT_DOMAINS)
    
    def _fetch_endpoint(self, subreddit: str, endpoint: str, params: dict, 
                        max_pages: int = 10) -> List[Dict]:
        
        posts = []
        after = None
        base_url = f"https://www.reddit.com/r/{subreddit}/{endpoint}.json"
        
        for page in range(max_pages):
            req_params = {'limit': 100, **params}
            if after:
                req_params['after'] = after
            
            try:
                response = self.session.get(base_url, params=req_params, timeout=15)
                
                if response.status_code == 429:
                    print(f"    ⏳ Rate limited, waiting 60s...")
                    time.sleep(60)
                    continue
                
                if response.status_code != 200:
                    break
                
                data = response.json()
                page_posts = data.get('data', {}).get('children', [])
                
                if not page_posts:
                    break
                
                posts.extend(page_posts)
                after = data.get('data', {}).get('after')
                
                if not after:
                    break
                
                time.sleep(2)
                
            except Exception as e:
                print(f"    ⚠️ Error: {e}")
                break
        
        return posts
    
    def scrape_subreddit_full(self, subreddit: str, days_back: int = None,
                             since_timestamp: float = None) -> Dict:
        
        cutoff_ts = None
        if days_back:
            cutoff_ts = (datetime.now(timezone.utc) - timedelta(days=days_back)).timestamp()
        elif since_timestamp:
            cutoff_ts = since_timestamp
        
        print(f"\n🔍 Scraping r/{subreddit}...")
        
        all_posts = {}
        
        for endpoint, params in self.ENDPOINTS:
            endpoint_name = f"{endpoint}" + (f"/{params.get('t', '')}" if params.get('t') else "")
            print(f"  📡 Fetching /{endpoint_name}...")
            
            posts = self._fetch_endpoint(subreddit, endpoint, params)
            
            new_posts = 0
            for post_data in posts:
                post = post_data['data']
                post_id = post['id']
                post_time = post.get('created_utc', 0)
                
                if cutoff_ts and post_time < cutoff_ts:
                    continue
                
                if post_id not in all_posts:
                    all_posts[post_id] = post
                    new_posts += 1
            
            print(f"    Found {len(posts)} posts, {new_posts} new unique")
            time.sleep(1)
        
        print(f"\n  💾 Processing {len(all_posts)} unique posts...")
        
        new_urls = 0
        duplicates = 0
        oldest_date = None
        newest_date = None
        
        for post_id, post in all_posts.items():
            post_time = post.get('created_utc', 0)
            post_date = datetime.fromtimestamp(post_time, timezone.utc)
            
            if oldest_date is None or post_date < oldest_date:
                oldest_date = post_date
            if newest_date is None or post_date > newest_date:
                newest_date = post_date
            
            urls = self.extract_urls_from_text(post.get('title', ''))
            urls.update(self.extract_urls_from_text(post.get('selftext', '')))
            
            post_url = post.get('url', '')
            if post_url and not self._is_reddit_url(post_url):
                urls.add(post_url)
            
            for url in urls:
                if self.db.add_url(url, subreddit, post_date.replace(tzinfo=None), post_id):
                    new_urls += 1
                else:
                    duplicates += 1
        
        stats = {
            'posts_processed': len(all_posts),
            'new_urls': new_urls,
            'duplicates': duplicates,
            'oldest_date': oldest_date,
            'newest_date': newest_date
        }
        
        date_range = ""
        if oldest_date and newest_date:
            days_covered = (newest_date - oldest_date).days
            date_range = f" ({oldest_date.strftime('%Y-%m-%d')} to {newest_date.strftime('%Y-%m-%d')}, {days_covered} days)"
        
        print(f"  ✅ r/{subreddit}: {len(all_posts)} posts, {new_urls} new URLs, {duplicates} duplicates{date_range}")
        
        return stats
    
    def scrape_subreddit_daily(self, subreddit: str) -> Dict:
        
        last_ts = self.db.get_last_scrape_timestamp(subreddit)
        
        if last_ts:
            last_date = datetime.fromtimestamp(last_ts, timezone.utc)
            print(f"\n🔍 Daily scrape r/{subreddit} (since {last_date.strftime('%Y-%m-%d %H:%M')} UTC)...")
        else:
            print(f"\n🔍 First daily scrape r/{subreddit} (last 24 hours)...")
            last_ts = (datetime.now(timezone.utc) - timedelta(days=1)).timestamp()
        
        posts = self._fetch_endpoint(subreddit, 'new', {}, max_pages=10)
        
        new_urls = 0
        duplicates = 0
        posts_in_range = 0
        
        for post_data in posts:
            post = post_data['data']
            post_time = post.get('created_utc', 0)
            
            if post_time < last_ts:
                continue
            
            posts_in_range += 1
            post_date = datetime.fromtimestamp(post_time, timezone.utc)
            post_id = post['id']
            
            urls = self.extract_urls_from_text(post.get('title', ''))
            urls.update(self.extract_urls_from_text(post.get('selftext', '')))
            
            post_url = post.get('url', '')
            if post_url and not self._is_reddit_url(post_url):
                urls.add(post_url)
            
            for url in urls:
                if self.db.add_url(url, subreddit, post_date.replace(tzinfo=None), post_id):
                    new_urls += 1
                else:
                    duplicates += 1
        
        self.db.update_last_scrape(subreddit)
        
        print(f"  ✅ r/{subreddit}: {posts_in_range} new posts, {new_urls} new URLs, {duplicates} duplicates")
        
        return {
            'posts_processed': posts_in_range,
            'new_urls': new_urls,
            'duplicates': duplicates
        }
    
    def backfill(self, subreddits: List[str], days: int):
        
        print(f"\n{'='*60}")
        print(f"🔄 BACKFILL MODE - Last {days} days")
        print(f"   Using multiple endpoints for maximum coverage")
        print(f"{'='*60}")
        
        total_urls = 0
        total_posts = 0
        
        for subreddit in subreddits:
            stats = self.scrape_subreddit_full(subreddit, days_back=days)
            total_urls += stats['new_urls']
            total_posts += stats['posts_processed']
        
        print(f"\n{'='*60}")
        print(f"✨ SUMMARY")
        print(f"   Posts processed: {total_posts}")
        print(f"   New URLs found: {total_urls}")
        print(f"{'='*60}\n")
        
        return total_urls
    
    def daily_update(self, subreddits: List[str]):
        
        print(f"\n{'='*60}")
        print(f"📅 DAILY MODE")
        print(f"{'='*60}")
        
        total_urls = 0
        
        for subreddit in subreddits:
            stats = self.scrape_subreddit_daily(subreddit)
            total_urls += stats['new_urls']
        
        print(f"\n{'='*60}")
        print(f"✨ Total new URLs found: {total_urls}")
        print(f"{'='*60}\n")
        
        return total_urls
    
    def export_csv(self, output_file='reddit_urls.csv'):
        
        count = self.db.export_to_csv(output_file)
        print(f"✅ Exported {count} URLs to {output_file}")
        return count
    
    def get_stats(self):
        
        stats = self.db.get_stats()
        
        print(f"\n{'='*60}")
        print(f"📊 DATABASE STATISTICS")
        print(f"{'='*60}")
        print(f"Total URLs: {stats['total_urls']}")
        print(f"Subreddits tracked: {stats['subreddit_count']}")
        print(f"Date range: {stats['earliest_post']} to {stats['latest_post']}")
        print(f"{'='*60}\n")

def main():
    parser = argparse.ArgumentParser(
        description='Reddit URL Scraper - Multi-endpoint for maximum historical data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=""
    )
    
    parser.add_argument('--backfill', type=int, metavar='DAYS',
                       help='Backfill mode: scrape last N days (uses all endpoints)')
    parser.add_argument('--daily', action='store_true',
                       help='Daily mode: scrape new posts since last run')
    parser.add_argument('--subreddits', nargs='+', metavar='SUB',
                       help='List of subreddits to scrape')
    parser.add_argument('--export', metavar='FILE',
                       help='Export URLs to CSV file')
    parser.add_argument('--stats', action='store_true',
                       help='Show database statistics')
    
    args = parser.parse_args()
    
    if args.backfill and args.daily:
        print("❌ Error: Cannot use --backfill and --daily together")
        sys.exit(1)
    
    if (args.backfill or args.daily) and not args.subreddits:
        print("❌ Error: --subreddits required")
        sys.exit(1)
    
    if not any([args.backfill, args.daily, args.export, args.stats]):
        parser.print_help()
        sys.exit(0)
    
    try:
        scraper = RedditURLScraperNoAuth()
        
        if args.backfill:
            scraper.backfill(args.subreddits, args.backfill)
        
        if args.daily:
            scraper.daily_update(args.subreddits)
        
        if args.export:
            scraper.export_csv(args.export)
        
        if args.stats:
            scraper.get_stats()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
