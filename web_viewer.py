#!/usr/bin/env python3
import os
from flask import Flask, render_template, jsonify, request, Response
import threading
import subprocess
from database import Database

# Change to script directory to find database
os.chdir(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)

scrape_state = {
    'running': False,
    'log': [],
    'urls_found': 0,
    'error': None
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
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    search = request.args.get('search', '')
    subreddit = request.args.get('subreddit', '')
    
    db = Database()
    result = db.get_urls(page=page, per_page=per_page, search=search if search else None, subreddit=subreddit if subreddit else None)
    db.close()
    return jsonify(result)

@app.route('/api/subreddits')
def get_subreddits():
    db = Database()
    subreddits = db.get_subreddits()
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
    mode = data.get('mode', 'daily')
    days = data.get('days', 7)
    subreddits = data.get('subreddits', ['SideProject'])
    
    def run_in_thread():
        global scrape_state
        scrape_state = {'running': True, 'log': [], 'urls_found': 0, 'error': None}
        
        try:
            cmd = ['python', 'reddit_scraper_noauth.py']
            if mode == 'backfill':
                cmd.extend(['--backfill', str(days)])
            else:
                cmd.append('--daily')
            cmd.extend(['--subreddits'] + subreddits)
            
            scrape_state['log'].append(f"Running: {' '.join(cmd)}")
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            for line in process.stdout:
                line = line.strip()
                if line:
                    scrape_state['log'].append(line)
                    if 'new URLs' in line.lower() or 'urls found' in line.lower():
                        try:
                            import re
                            nums = re.findall(r'\d+', line)
                            if nums:
                                scrape_state['urls_found'] = int(nums[0])
                        except:
                            pass
            
            process.wait()
            
            if process.returncode != 0:
                scrape_state['error'] = f'Process exited with code {process.returncode}'
            
            scrape_state['log'].append("Completed!")
            
        except Exception as e:
            scrape_state['error'] = str(e)
            scrape_state['log'].append(f"Error: {str(e)}")
        finally:
            scrape_state['running'] = False
    
    thread = threading.Thread(target=run_in_thread)
    thread.daemon = True
    thread.start()
    
    return jsonify({'status': 'started'})

@app.route('/api/export')
def export_csv():
    db = Database()
    import io
    import csv
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['url', 'post_date', 'subreddit', 'post_id'])
    
    cursor = db.conn.cursor()
    cursor.execute("SELECT url, post_date, subreddit, post_id FROM urls ORDER BY post_date DESC")
    for row in cursor.fetchall():
        writer.writerow([row['url'], row['post_date'], row['subreddit'], row['post_id']])
    
    db.close()
    
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=reddit_urls.csv'}
    )

if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("🔗 Reddit URL Scraper")
    print("=" * 50)
    print("\n🚀 http://localhost:3010\n")
    app.run(host='0.0.0.0', port=3010, debug=True)
