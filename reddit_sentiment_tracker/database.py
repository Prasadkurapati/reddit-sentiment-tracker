import sqlite3
import pandas as pd
from datetime import datetime
import json

def init_db(db_path='sentiment.db'):
    """Initialize SQLite database with tables"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Raw posts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            score INTEGER,
            created_utc TIMESTAMP,
            url TEXT UNIQUE,
            num_comments INTEGER,
            fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Sentiment analysis results
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sentiment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER,
            sentiment_label TEXT,
            sentiment_score REAL,
            sentiment_value INTEGER,
            analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES posts (id)
        )
    ''')
    
    # Ticker mentions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mentions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER,
            ticker TEXT,
            FOREIGN KEY (post_id) REFERENCES posts (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database initialized at {db_path}")

def load_csv_to_db(csv_path, db_path='sentiment.db'):
    """Load processed CSV into database"""
    df = pd.read_csv(csv_path)
    conn = sqlite3.connect(db_path)
    
    for _, row in df.iterrows():
        try:
            # Insert post
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO posts (title, score, created_utc, url, num_comments)
                VALUES (?, ?, ?, ?, ?)
            ''', (row['title'], row['score'], row['created_utc'], row['url'], row.get('num_comments', 0)))
            
            # Get post_id
            cursor.execute('SELECT id FROM posts WHERE url = ?', (row['url'],))
            post_id = cursor.fetchone()[0]
            
            # Insert sentiment
            cursor.execute('''
                INSERT INTO sentiment (post_id, sentiment_label, sentiment_score, sentiment_value)
                VALUES (?, ?, ?, ?)
            ''', (post_id, row['sentiment_label'], row['sentiment_score'], row['sentiment_value']))
            
            # Insert tickers
            tickers = eval(row['tickers']) if isinstance(row['tickers'], str) else row['tickers']
            for ticker in tickers:
                cursor.execute('INSERT INTO mentions (post_id, ticker) VALUES (?, ?)', 
                             (post_id, ticker))
                
        except Exception as e:
            print(f"Error processing row: {e}")
            continue
    
    conn.commit()
    conn.close()
    print(f"Loaded data from {csv_path}")

def get_ticker_sentiment(ticker, db_path='sentiment.db'):
    """Query average sentiment for a specific ticker"""
    conn = sqlite3.connect(db_path)
    query = '''
        SELECT 
            m.ticker,
            COUNT(DISTINCT p.id) as mention_count,
            AVG(s.sentiment_value) as avg_sentiment,
            AVG(s.sentiment_score) as avg_confidence,
            MAX(p.created_utc) as last_mention
        FROM mentions m
        JOIN posts p ON m.post_id = p.id
        JOIN sentiment s ON p.id = s.post_id
        WHERE m.ticker = ?
        GROUP BY m.ticker
    '''
    result = pd.read_sql_query(query, conn, params=(ticker,))
    conn.close()
    return result

def get_all_tickers(db_path='sentiment.db'):
    """Get sentiment summary for all tickers"""
    conn = sqlite3.connect(db_path)
    query = '''
        SELECT 
            m.ticker,
            COUNT(DISTINCT p.id) as mention_count,
            AVG(s.sentiment_value) as avg_sentiment,
            AVG(s.sentiment_score) as avg_confidence
        FROM mentions m
        JOIN posts p ON m.post_id = p.id
        JOIN sentiment s ON p.id = s.post_id
        GROUP BY m.ticker
        ORDER BY mention_count DESC
    '''
    result = pd.read_sql_query(query, conn)
    conn.close()
    return result

if __name__ == '__main__':
    init_db()
    load_csv_to_db('posts_with_sentiment.csv')
    
    print("\n=== All Tickers Sentiment ===")
    print(get_all_tickers())
    
    print("\n=== MSFT Specific ===")
    print(get_ticker_sentiment('MSFT'))