#!/usr/bin/env python3

import sqlite3
import csv
from datetime import datetime
from typing import Optional, Dict, Any

class Database:
    
    
    def __init__(self, db_path='reddit_urls.db'):
        
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()
    
    def _create_tables(self):
        
        cursor = self.conn.cursor()
        
        cursor.execute()
        
        cursor.execute()
        
        cursor.execute()
        
        cursor.execute()
        
        self.conn.commit()
    
    def add_url(self, url: str, subreddit: str, post_date: datetime, 
                post_id: str) -> bool:
        
        cursor = self.conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO urls (url, subreddit, post_id, post_date) 
                VALUES (?, ?, ?, ?)
            """, (url, subreddit, post_id, post_date))
            
            self.conn.commit()
            return True
            
        except sqlite3.IntegrityError:
            return False
    
    def get_last_scrape_timestamp(self, subreddit: str) -> Optional[float]:
        
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT last_scrape_timestamp FROM last_scrape WHERE subreddit = ?
        """, (subreddit,))
        
        row = cursor.fetchone()
        return row['last_scrape_timestamp'] if row else None
    
    def update_last_scrape(self, subreddit: str):
        
        cursor = self.conn.cursor()
        timestamp = datetime.utcnow().timestamp()
        
        cursor.execute("""
            INSERT OR REPLACE INTO last_scrape (subreddit, last_scrape_timestamp)
            VALUES (?, ?)
        """, (subreddit, timestamp))
        
        self.conn.commit()
    
    def export_to_csv(self, output_file: str) -> int:
        
        cursor = self.conn.cursor()
        
        cursor.execute()
        
        rows = cursor.fetchall()
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            writer.writerow(['url', 'post_date', 'subreddit', 'post_id'])
            
            for row in rows:
                writer.writerow([
                    row['url'],
                    row['post_date'],
                    row['subreddit'],
                    row['post_id']
                ])
        
        return len(rows)
    
    def get_stats(self) -> Dict[str, Any]:
        
        cursor = self.conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as count FROM urls")
        total_urls = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(DISTINCT subreddit) as count FROM urls")
        subreddit_count = cursor.fetchone()['count']
        
        cursor.execute()
        date_range = cursor.fetchone()
        
        return {
            'total_urls': total_urls,
            'subreddit_count': subreddit_count,
            'earliest_post': date_range['earliest'] or 'N/A',
            'latest_post': date_range['latest'] or 'N/A'
        }
    
    def close(self):
        
        self.conn.close()
    
    def __enter__(self):
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        
        self.close()
