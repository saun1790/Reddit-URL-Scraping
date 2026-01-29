#!/usr/bin/env python3

from flask import Flask, render_template, jsonify, request, Response
from database import Database
from datetime import datetime
import os
import sys
import subprocess
import threading
import time
import io
import csv

app = Flask(__name__)

scrape_state = {
    'running': False,
    'progress': 0,
    'current_sub': '',
    'total_subs': 0,
    'completed_subs': 0,
    'urls_found': 0,
    'started_at': None,
    'error': None,
    'log': []
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stats')
def get_stats():
    db = Database()
    stats = db.get_stats()
    db.close()
    return jsonify(stats)

@app.route('/api/urls')
def get_urls():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 50))
    subreddit = request.args.get('subreddit', None)
    search = request.args.get('search', None)
    
    db = Database()
    cursor = db.conn.cursor()
    
    conditions = []
    params = []
    
    if subreddit:
        conditions.append("subreddit = ?")
        params.append(subreddit)
    
    if search:
        conditions.append("(url LIKE ? OR subreddit LIKE ?)")
        params.extend([f'%{search}%', f'%{search}%'])
    
    where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    
    cursor.execute(f"SELECT COUNT(*) as count FROM urls {where}", params)
    total = cursor.fetchone()['count']
    
    query = f
    params.extend([per_page, (page - 1) * per_page])
    cursor.execute(query, params)
    urls = [dict(row) for row in cursor.fetchall()]
    
    db.close()
    
    return jsonify({
        'urls': urls,
        'page': page,
        'per_page': per_page,
        'total': total,
        'pages': max(1, (total + per_page - 1) // per_page)
    })

@app.route('/api/subreddits')
def get_subreddits():
    db = Database()
    cursor = db.conn.cursor()
    cursor.execute()
    subreddits = [dict(row) for row in cursor.fetchall()]
    db.close()
    return jsonify(subreddits)

@app.route('/api/scrape/status')
def scrape_status():
    return jsonify(scrape_state)

@app.route('/api/scrape/run', methods=['POST'])
def run_scraper():
    global scrape_state
    
    if scrape_state['running']:
        return jsonify({'error': 'Already running'}), 400
    
    data = request.json
    subreddits = data.get('subreddits', [])
    mode = data.get('mode', 'daily')
    days = data.get('days', 7)
    
    if not subreddits:
        return jsonify({'error': 'No subreddits configured'}), 400
    
    def run():
        global scrape_state
        scrape_state = {
            'running': True,
            'progress': 0,
            'current_sub': '',
            'total_subs': len(subreddits),
            'completed_subs': 0,
            'urls_found': 0,
            'started_at': datetime.now().isoformat(),
            'error': None,
            'log': [f"Starting scrape: {len(subreddits)} subreddit(s), mode={mode}, days={days}"]
        }
        
        try:
            venv_python = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                'venv', 'bin', 'python'
            )
            python_cmd = venv_python if os.path.exists(venv_python) else sys.executable
            
            db = Database()
            cursor = db.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM urls")
            initial_count = cursor.fetchone()[0]
            db.close()
            
            for i, sub in enumerate(subreddits):
                scrape_state['current_sub'] = sub
                scrape_state['progress'] = int((i / len(subreddits)) * 100)
                scrape_state['log'].append(f"📡 Scraping r/{sub}...")
                
                cmd = [python_cmd, 'reddit_scraper_noauth.py']
                if mode == 'daily':
                    cmd.append('--daily')
                else:
                    cmd.extend(['--backfill', str(days)])
                cmd.extend(['--subreddits', sub])
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    cwd=os.path.dirname(os.path.abspath(__file__)),
                    timeout=600
                )
                
                scrape_state['completed_subs'] = i + 1
                
                output = result.stdout if result.stdout else ""
                if result.returncode != 0:
                    error_msg = result.stderr[:300] if result.stderr else "Unknown error"
                    scrape_state['log'].append(f"⚠️ Error on r/{sub}: {error_msg}")
                else:
                    for line in output.split('\n'):
                        if '✅' in line or '⚠️' in line:
                            scrape_state['log'].append(line.strip())
                            break
                    else:
                        scrape_state['log'].append(f"✓ Completed r/{sub}")
                
                time.sleep(2)
            
            db = Database()
            cursor = db.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM urls")
            final_count = cursor.fetchone()[0]
            db.close()
            
            scrape_state['urls_found'] = final_count - initial_count
            scrape_state['progress'] = 100
            scrape_state['log'].append(f"✅ Done! Found {scrape_state['urls_found']} new URLs")
            
        except subprocess.TimeoutExpired:
            scrape_state['error'] = "Timeout"
            scrape_state['log'].append("❌ Timeout")
        except Exception as e:
            scrape_state['error'] = str(e)
            scrape_state['log'].append(f"❌ Error: {str(e)}")
        finally:
            scrape_state['running'] = False
    
    thread = threading.Thread(target=run)
    thread.start()
    
    return jsonify({'message': 'Started', 'total': len(subreddits)})

@app.route('/api/export')
def export_csv():
    db = Database()
    cursor = db.conn.cursor()
    cursor.execute("SELECT url, post_date, subreddit, post_id FROM urls ORDER BY post_date DESC")
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['url', 'post_date', 'subreddit', 'post_id'])
    for row in cursor.fetchall():
        writer.writerow([row['url'], row['post_date'], row['subreddit'], row['post_id']])
    
    db.close()
    
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=reddit_urls.csv'}
    )

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🔗 Reddit URL Scraper")
    print("="*50)
    print("\n🚀 http://localhost:3010\n")
    app.run(debug=True, host='0.0.0.0', port=3010)
