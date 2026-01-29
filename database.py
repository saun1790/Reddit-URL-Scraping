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
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                subreddit TEXT NOT NULL,
                post_id TEXT NOT NULL,
                post_date TIMESTAMP NOT NULL,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(url, subreddit, post_id)
            )
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_subreddit ON urls(subreddit)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_post_date ON urls(post_date DESC)
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS last_scrape (
                subreddit TEXT PRIMARY KEY,
                last_scrape_timestamp REAL
            )
        """)
        self.conn.commit()
    
    def add_url(self, url: str, subreddit: str, post_date: datetime, post_id: str) -> bool:
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO urls (url, subreddit, post_id, post_date) VALUES (?, ?, ?, ?)
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
            INSERT OR REPLACE INTO last_scrape (subreddit, last_scrape_timestamp) VALUES (?, ?)
        """, (subreddit, timestamp))
        self.conn.commit()
    
    def export_to_csv(self, output_file: str) -> int:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT url, post_date, subreddit, post_id FROM urls ORDER BY post_date DESC
        """)
        rows = cursor.fetchall()
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['url', 'post_date', 'subreddit', 'post_id'])
            for row in rows:
                writer.writerow([row['url'], row['post_date'], row['subreddit'], row['post_id']])
        return len(rows)
    
    def get_stats(self) -> Dict[str, Any]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) as total FROM urls")
        total = cursor.fetchone()['total']
        cursor.execute("SELECT COUNT(DISTINCT subreddit) as subs FROM urls")
        subs = cursor.fetchone()['subs']
        cursor.execute("SELECT MIN(post_date) as oldest, MAX(post_date) as newest FROM urls")
        row = cursor.fetchone()
        return {
            'total_urls': total,
            'subreddits': subs,
            'oldest_post': row['oldest'],
            'newest_post': row['newest']
        }
    
    def get_urls(self, page: int = 1, per_page: int = 50, subreddit: str = None, search: str = None):
        cursor = self.conn.cursor()
        offset = (page - 1) * per_page
        where_clauses = []
        params = []
        if subreddit:
            where_clauses.append("subreddit = ?")
            params.append(subreddit)
        if search:
            where_clauses.append("(url LIKE ? OR post_id LIKE ?)")
            params.extend([f'%{search}%', f'%{search}%'])
        where_sql = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""
        cursor.execute(f"SELECT COUNT(*) as total FROM urls{where_sql}", params)
        total = cursor.fetchone()['total']
        cursor.execute(f"""
            SELECT * FROM urls{where_sql} ORDER BY post_date DESC LIMIT ? OFFSET ?
        """, params + [per_page, offset])
        rows = cursor.fetchall()
        return {
            'urls': [dict(row) for row in rows],
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page
        }
    
    def get_subreddits(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT subreddit, COUNT(*) as count FROM urls GROUP BY subreddit ORDER BY count DESC
        """)
        return [{'name': row['subreddit'], 'count': row['count']} for row in cursor.fetchall()]
    
    def close(self):
        self.conn.close()
