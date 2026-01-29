#!/usr/bin/env python3
import os
import sys
import functools
from flask import Flask, render_template, jsonify, request, Response, session, redirect, url_for
import threading
import subprocess
from database import Database

# Change to script directory to find database
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

# Get Python executable from same venv
PYTHON_EXE = sys.executable

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'reddit-scraper-secret-key-2026')

# ============================================
# AUTHENTICATION (uses .env in production)
# ============================================
USERS = {
    os.environ.get('ADMIN_USERNAME', 'admin'): os.environ.get('ADMIN_PASSWORD', 'gwF1cZePMdTFd4Ls')
}

def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            if request.is_json or request.path.startswith('/api/'):
                return jsonify({'error': 'Unauthorized'}), 401
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if username in USERS and USERS[username] == password:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('index'))
        error = 'Invalid credentials'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ============================================
# MAIN ROUTES (Protected)
# ============================================
scrape_state = {
    'running': False,
    'log': [],
    'urls_found': 0,
    'error': None
}

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/api/stats')
@login_required
def get_stats():
    subreddit = request.args.get('subreddit', '')
    search = request.args.get('search', '')
    db = Database()
    stats = db.get_stats(
        subreddit=subreddit if subreddit else None,
        search=search if search else None
    )
    db.close()
    return jsonify(stats)

@app.route('/api/urls')
@login_required
def get_urls():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    search = request.args.get('search', '')
    subreddit = request.args.get('subreddit', '')
    sort = request.args.get('sort', 'post_date')
    order = request.args.get('order', 'desc')
    
    db = Database()
    result = db.get_urls(page=page, per_page=per_page, search=search if search else None, subreddit=subreddit if subreddit else None, sort=sort, order=order)
    db.close()
    return jsonify(result)

@app.route('/api/subreddits')
@login_required
def get_subreddits():
    db = Database()
    subreddits = db.get_subreddits()
    db.close()
    return jsonify(subreddits)

@app.route('/api/scrape/status')
@login_required
def scrape_status():
    return jsonify(scrape_state)

@app.route('/api/scrape/run', methods=['POST'])
@login_required
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
            scraper_path = os.path.join(SCRIPT_DIR, 'reddit_scraper_noauth.py')
            cmd = [PYTHON_EXE, scraper_path]
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
                bufsize=1,
                cwd=SCRIPT_DIR
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
@login_required
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

@app.route('/api/urls/<int:url_id>', methods=['PUT'])
@login_required
def update_url(url_id):
    data = request.json
    new_url = data.get('url')
    if not new_url:
        return jsonify({'error': 'URL required'}), 400
    
    db = Database()
    cursor = db.conn.cursor()
    cursor.execute("UPDATE urls SET url = ? WHERE id = ?", (new_url, url_id))
    db.conn.commit()
    affected = cursor.rowcount
    db.close()
    
    if affected == 0:
        return jsonify({'error': 'URL not found'}), 404
    return jsonify({'success': True})

@app.route('/api/urls/<int:url_id>', methods=['DELETE'])
@login_required
def delete_url(url_id):
    db = Database()
    cursor = db.conn.cursor()
    cursor.execute("DELETE FROM urls WHERE id = ?", (url_id,))
    db.conn.commit()
    affected = cursor.rowcount
    db.close()
    
    if affected == 0:
        return jsonify({'error': 'URL not found'}), 404
    return jsonify({'success': True})

@app.route('/api/urls/fix-malformed', methods=['POST'])
@login_required
def fix_malformed_urls():
    import sqlite3
    conn = sqlite3.connect('reddit_urls.db', timeout=30)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id, url, subreddit, post_id FROM urls WHERE url LIKE '%](%'")
        rows = cursor.fetchall()
        
        fixed = 0
        deleted = 0
        
        for row in rows:
            url = row['url']
            if '](http' in url:
                parts = url.split('](')
                if len(parts) >= 2:
                    clean_url = parts[1].rstrip(')')
                    clean_url = clean_url.split(')')[0].split('<')[0].split('!')[0]
                    if clean_url.startswith('http'):
                        cursor.execute(
                            "SELECT id FROM urls WHERE url = ? AND subreddit = ? AND post_id = ?",
                            (clean_url, row['subreddit'], row['post_id'])
                        )
                        existing = cursor.fetchone()
                        if existing:
                            cursor.execute("DELETE FROM urls WHERE id = ?", (row['id'],))
                            deleted += 1
                        else:
                            cursor.execute("UPDATE urls SET url = ? WHERE id = ?", (clean_url, row['id']))
                            fixed += 1
                    else:
                        cursor.execute("DELETE FROM urls WHERE id = ?", (row['id'],))
                        deleted += 1
            else:
                cursor.execute("DELETE FROM urls WHERE id = ?", (row['id'],))
                deleted += 1
        
        conn.commit()
        return jsonify({'fixed': fixed, 'deleted': deleted})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    # Load .env file if exists (for local development)
    env_file = os.path.join(SCRIPT_DIR, '.env')
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ.setdefault(key.strip(), value.strip())
    
    debug_mode = os.environ.get('DEBUG', 'true').lower() == 'true'
    
    print("\n" + "=" * 50)
    print("🔗 Reddit URL Scraper")
    print("=" * 50)
    print(f"\n🔐 Login: {os.environ.get('ADMIN_USERNAME', 'admin')} / {os.environ.get('ADMIN_PASSWORD', 'gwF1cZePMdTFd4Ls')}")
    print("🚀 http://localhost:3010\n")
    app.run(host='0.0.0.0', port=3010, debug=debug_mode)
