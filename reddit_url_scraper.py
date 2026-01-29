#!/usr/bin/env python3
"""
Reddit URL Scraper - Extract external URLs from subreddit posts
Uses Reddit API (PRAW) to fetch posts and extract external links
"""
import praw
import re
from datetime import datetime, timedelta
from typing import List, Set
import argparse
import sys
from database import Database
from config import load_config


class RedditURLScraper:
    """Scrapes external URLs from Reddit subreddits"""
    
    # Regex to extract URLs from text
    URL_PATTERN = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    )
    
    # Reddit domains to ignore
    REDDIT_DOMAINS = {
        'reddit.com',
        'www.reddit.com',
        'old.reddit.com',
        'new.reddit.com',
        'redd.it',
        'i.redd.it',
        'v.redd.it',
        'reddit.app.link',
        'preview.redd.it',
        'redditads.com'
    }
    
    def __init__(self, config_path='config.ini'):
        """Initialize the scraper with Reddit API credentials"""
        config = load_config(config_path)
        
        self.reddit = praw.Reddit(
            client_id=config['client_id'],
            client_secret=config['client_secret'],
            user_agent=config['user_agent']
        )
        
        self.db = Database()
    
    def extract_urls_from_text(self, text: str) -> Set[str]:
        """Extract and normalize URLs from text"""
        if not text:
            return set()
        
        urls = self.URL_PATTERN.findall(text)
        normalized_urls = set()
        
        for url in urls:
            # Normalize URL: strip trailing punctuation
            url = url.rstrip('.,;:!?)]\'"')
            
            # Check if it's not a Reddit internal link
            if not self._is_reddit_url(url):
                normalized_urls.add(url)
        
        return normalized_urls
    
    def _is_reddit_url(self, url: str) -> bool:
        """Check if URL is a Reddit internal link"""
        url_lower = url.lower()
        for domain in self.REDDIT_DOMAINS:
            if domain in url_lower:
                return True
        return False
    
    def scrape_subreddit(self, subreddit_name: str, days_back: int = None, 
                        since_timestamp: float = None) -> int:
        """
        Scrape URLs from a subreddit
        
        Args:
            subreddit_name: Name of the subreddit (without r/)
            days_back: Number of days to look back (for backfill mode)
            since_timestamp: Unix timestamp to fetch posts since (for daily mode)
        
        Returns:
            Number of new URLs found
        """
        subreddit = self.reddit.subreddit(subreddit_name)
        new_urls_count = 0
        
        # Determine time cutoff
        if days_back:
            cutoff_date = datetime.utcnow() - timedelta(days=days_back)
            cutoff_timestamp = cutoff_date.timestamp()
        elif since_timestamp:
            cutoff_timestamp = since_timestamp
        else:
            # Default: last 24 hours
            cutoff_timestamp = (datetime.utcnow() - timedelta(days=1)).timestamp()
        
        print(f"\n🔍 Scraping r/{subreddit_name}...")
        posts_processed = 0
        
        try:
            # Fetch posts (using 'new' to get chronological order)
            for post in subreddit.new(limit=None):
                # Check if post is within our time window
                if post.created_utc < cutoff_timestamp:
                    break
                
                posts_processed += 1
                
                # Extract URLs from title and selftext
                urls = self.extract_urls_from_text(post.title)
                urls.update(self.extract_urls_from_text(post.selftext))
                
                # Also check the post URL itself if it's a link post
                if hasattr(post, 'url') and post.url:
                    url_set = self.extract_urls_from_text(post.url)
                    if url_set:
                        urls.update(url_set)
                    elif not self._is_reddit_url(post.url):
                        urls.add(post.url)
                
                # Store URLs in database
                post_date = datetime.utcfromtimestamp(post.created_utc)
                
                for url in urls:
                    if self.db.add_url(url, subreddit_name, post_date, post.id):
                        new_urls_count += 1
                
                # Progress indicator
                if posts_processed % 100 == 0:
                    print(f"  Processed {posts_processed} posts, found {new_urls_count} new URLs...")
            
            print(f"✅ r/{subreddit_name}: {posts_processed} posts processed, {new_urls_count} new URLs found")
            
        except Exception as e:
            print(f"❌ Error scraping r/{subreddit_name}: {e}")
            return new_urls_count
        
        return new_urls_count
    
    def backfill(self, subreddits: List[str], days: int):
        """Backfill mode: scrape posts from the last N days"""
        print(f"\n{'='*60}")
        print(f"🔄 BACKFILL MODE - Last {days} days")
        print(f"{'='*60}")
        
        total_urls = 0
        for subreddit in subreddits:
            count = self.scrape_subreddit(subreddit, days_back=days)
            total_urls += count
        
        print(f"\n{'='*60}")
        print(f"✨ Total new URLs found: {total_urls}")
        print(f"{'='*60}\n")
        
        return total_urls
    
    def daily_update(self, subreddits: List[str]):
        """Daily mode: scrape new posts since last run"""
        print(f"\n{'='*60}")
        print(f"📅 DAILY MODE")
        print(f"{'='*60}")
        
        total_urls = 0
        for subreddit in subreddits:
            # Get last scrape timestamp for this subreddit
            last_timestamp = self.db.get_last_scrape_timestamp(subreddit)
            
            if last_timestamp:
                last_date = datetime.utcfromtimestamp(last_timestamp)
                print(f"  Last scrape for r/{subreddit}: {last_date.strftime('%Y-%m-%d %H:%M:%S')} UTC")
            else:
                print(f"  First time scraping r/{subreddit} (will fetch last 24 hours)")
                last_timestamp = (datetime.utcnow() - timedelta(days=1)).timestamp()
            
            count = self.scrape_subreddit(subreddit, since_timestamp=last_timestamp)
            total_urls += count
            
            # Update last scrape timestamp
            self.db.update_last_scrape(subreddit)
        
        print(f"\n{'='*60}")
        print(f"✨ Total new URLs found: {total_urls}")
        print(f"{'='*60}\n")
        
        return total_urls
    
    def export_csv(self, output_file='reddit_urls.csv'):
        """Export all URLs to CSV"""
        count = self.db.export_to_csv(output_file)
        print(f"✅ Exported {count} URLs to {output_file}")
        return count
    
    def get_stats(self):
        """Print database statistics"""
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
        description='Reddit URL Scraper - Extract external URLs from subreddits',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Backfill mode - get last 90 days from r/SideProject
  python reddit_url_scraper.py --backfill 90 --subreddits SideProject

  # Daily mode - get new posts from multiple subreddits
  python reddit_url_scraper.py --daily --subreddits SideProject startups entrepreneur

  # Export to CSV
  python reddit_url_scraper.py --export output.csv

  # Show statistics
  python reddit_url_scraper.py --stats
        """
    )
    
    parser.add_argument('--backfill', type=int, metavar='DAYS',
                       help='Backfill mode: scrape last N days')
    parser.add_argument('--daily', action='store_true',
                       help='Daily mode: scrape new posts since last run')
    parser.add_argument('--subreddits', nargs='+', metavar='SUB',
                       help='List of subreddits to scrape (without r/)')
    parser.add_argument('--export', metavar='FILE',
                       help='Export URLs to CSV file')
    parser.add_argument('--stats', action='store_true',
                       help='Show database statistics')
    parser.add_argument('--config', default='config.ini',
                       help='Path to config file (default: config.ini)')
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.backfill and args.daily:
        print("❌ Error: Cannot use --backfill and --daily together")
        sys.exit(1)
    
    if (args.backfill or args.daily) and not args.subreddits:
        print("❌ Error: --subreddits required for backfill or daily mode")
        sys.exit(1)
    
    if not any([args.backfill, args.daily, args.export, args.stats]):
        parser.print_help()
        sys.exit(0)
    
    try:
        scraper = RedditURLScraper(args.config)
        
        # Execute requested operation
        if args.backfill:
            scraper.backfill(args.subreddits, args.backfill)
        
        if args.daily:
            scraper.daily_update(args.subreddits)
        
        if args.export:
            scraper.export_csv(args.export)
        
        if args.stats:
            scraper.get_stats()
        
    except FileNotFoundError as e:
        print(f"❌ {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
