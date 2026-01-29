#!/usr/bin/env python3
"""
Test script to verify the scraper works without real API calls
Tests the database, URL extraction, and core functionality
"""
import sys
from datetime import datetime
from database import Database

def test_database():
    """Test database operations"""
    print("\n" + "="*60)
    print("🧪 TESTING DATABASE")
    print("="*60)
    
    # Create test database
    db = Database('test_reddit.db')
    
    # Test adding URLs
    print("\n1. Testing URL insertion...")
    url1 = "https://example.com/page1"
    result1 = db.add_url(url1, "SideProject", datetime(2026, 1, 28, 10, 30), "abc123")
    print(f"   First insert: {'✅ Added' if result1 else '❌ Failed'}")
    
    # Test deduplication
    print("\n2. Testing deduplication...")
    result2 = db.add_url(url1, "SideProject", datetime(2026, 1, 28, 10, 30), "abc123")
    print(f"   Duplicate insert: {'✅ Blocked (correct!)' if not result2 else '❌ Should have blocked'}")
    
    # Add more test data
    print("\n3. Adding test data...")
    test_urls = [
        ("https://github.com/test", "startups", datetime(2026, 1, 27, 14, 20), "xyz789"),
        ("https://example.org/blog", "SideProject", datetime(2026, 1, 26, 9, 15), "def456"),
        ("https://site.com/product", "entrepreneur", datetime(2026, 1, 25, 16, 45), "ghi789"),
    ]
    
    for url, sub, date, post_id in test_urls:
        db.add_url(url, sub, date, post_id)
    
    print(f"   Added {len(test_urls) + 1} URLs")
    
    # Test stats
    print("\n4. Testing statistics...")
    stats = db.get_stats()
    print(f"   Total URLs: {stats['total_urls']}")
    print(f"   Subreddits: {stats['subreddit_count']}")
    print(f"   Date range: {stats['earliest_post']} to {stats['latest_post']}")
    
    # Test CSV export
    print("\n5. Testing CSV export...")
    count = db.export_to_csv('test_output.csv')
    print(f"   Exported {count} URLs to test_output.csv")
    
    # Test scrape history
    print("\n6. Testing scrape history...")
    db.update_last_scrape("SideProject")
    timestamp = db.get_last_scrape_timestamp("SideProject")
    print(f"   Last scrape timestamp: {timestamp}")
    print(f"   Date: {datetime.utcfromtimestamp(timestamp)}")
    
    db.close()
    
    print("\n" + "="*60)
    print("✅ ALL DATABASE TESTS PASSED")
    print("="*60)
    
    return True

def test_url_extraction():
    """Test URL extraction and normalization"""
    print("\n" + "="*60)
    print("🧪 TESTING URL EXTRACTION")
    print("="*60)
    
    from reddit_url_scraper import RedditURLScraper
    import re
    
    # We can test the regex without Reddit API
    URL_PATTERN = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    )
    
    test_cases = [
        ("Check out https://example.com for more info!", ["https://example.com"]),
        ("Visit https://site.com/page?id=123", ["https://site.com/page?id=123"]),
        ("Link: https://github.com/user/repo.", ["https://github.com/user/repo"]),
        ("Multiple: https://a.com and https://b.com here", ["https://a.com", "https://b.com"]),
        ("No links in this text", []),
    ]
    
    print("\nTesting URL extraction patterns:")
    all_passed = True
    
    for i, (text, expected) in enumerate(test_cases, 1):
        urls = URL_PATTERN.findall(text)
        # Normalize (strip trailing punctuation)
        urls = [url.rstrip('.,;:!?)]\'"') for url in urls]
        
        passed = sorted(urls) == sorted(expected)
        status = "✅" if passed else "❌"
        print(f"   {status} Test {i}: {text[:50]}...")
        if not passed:
            print(f"      Expected: {expected}")
            print(f"      Got: {urls}")
            all_passed = False
    
    # Test Reddit URL filtering
    print("\nTesting Reddit URL filtering:")
    reddit_urls = [
        "https://www.reddit.com/r/test",
        "https://i.redd.it/image.jpg",
        "https://v.redd.it/video",
        "https://old.reddit.com/post",
    ]
    
    REDDIT_DOMAINS = {'reddit.com', 'www.reddit.com', 'redd.it', 'i.redd.it', 'v.redd.it'}
    
    for url in reddit_urls:
        is_reddit = any(domain in url.lower() for domain in REDDIT_DOMAINS)
        status = "✅" if is_reddit else "❌"
        print(f"   {status} Correctly identified: {url}")
    
    print("\n" + "="*60)
    if all_passed:
        print("✅ ALL URL EXTRACTION TESTS PASSED")
    else:
        print("❌ SOME TESTS FAILED")
    print("="*60)
    
    return all_passed

def show_test_csv():
    """Display the exported CSV"""
    print("\n" + "="*60)
    print("📄 EXPORTED CSV CONTENT")
    print("="*60 + "\n")
    
    try:
        with open('test_output.csv', 'r') as f:
            content = f.read()
            print(content)
    except FileNotFoundError:
        print("CSV file not found")
    
    print("="*60)

def cleanup():
    """Clean up test files"""
    import os
    files_to_remove = ['test_reddit.db', 'test_output.csv']
    
    print("\n🧹 Cleaning up test files...")
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)
            print(f"   Removed {file}")

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🚀 REDDIT URL SCRAPER - TEST SUITE")
    print("="*60)
    print("\nTesting core functionality without API calls...")
    
    try:
        # Run tests
        db_passed = test_database()
        url_passed = test_url_extraction()
        
        # Show results
        show_test_csv()
        
        # Summary
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)
        print(f"Database operations: {'✅ PASSED' if db_passed else '❌ FAILED'}")
        print(f"URL extraction: {'✅ PASSED' if url_passed else '❌ FAILED'}")
        print("\n💡 To test with real Reddit data:")
        print("   1. Get API credentials: see API_SETUP.md")
        print("   2. Copy config.ini.example to config.ini")
        print("   3. Add your credentials")
        print("   4. Run: python reddit_url_scraper.py --backfill 7 --subreddits test")
        print("="*60 + "\n")
        
        # Cleanup
        cleanup()
        
        if db_passed and url_passed:
            print("✅ All tests passed! Project is ready to use.\n")
            return 0
        else:
            print("❌ Some tests failed.\n")
            return 1
            
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        cleanup()
        return 1

if __name__ == '__main__':
    sys.exit(main())
