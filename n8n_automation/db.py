import sqlite3
from datetime import datetime

DB_PATH = 'logs/agentic_research.db'

# Initialize DB and tables
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS research_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        step TEXT,
        input TEXT,
        output TEXT,
        model TEXT,
        timestamp TEXT,
        status TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS tweets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        posted_at TEXT,
        engagement_stats TEXT,
        status TEXT
    )''')
    conn.commit()
    conn.close()

# Log an agent step
def log_agent_step(step, input_data, output_data, model, status='OK'):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO research_log (step, input, output, model, timestamp, status)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (step, str(input_data), str(output_data), model, datetime.utcnow().isoformat(), status))
    conn.commit()
    conn.close()

# Log a tweet
def log_tweet(text, posted_at, engagement_stats=None, status='POSTED'):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO tweets (text, posted_at, engagement_stats, status)
                 VALUES (?, ?, ?, ?)''',
              (text, posted_at, str(engagement_stats) if engagement_stats else '', status))
    conn.commit()
    conn.close()

# Fetch research logs
def fetch_research_logs(limit=100):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM research_log ORDER BY id DESC LIMIT ?', (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

# Fetch tweets
def fetch_tweets(limit=100):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM tweets ORDER BY id DESC LIMIT ?', (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

if __name__ == '__main__':
    init_db()
    print('DB initialized.') 