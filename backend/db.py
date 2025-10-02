import sqlite3
import json
import os
from typing import Dict, Optional
from contextlib import contextmanager

DB_PATH = os.getenv('DB_PATH', 'telegram_bot.db')

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def init_db():
    """Initialize database tables"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                email TEXT,
                tokens TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Events cache table (optional)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                event_id TEXT,
                title TEXT,
                start_time TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Notes cache table (optional)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                note_id TEXT,
                title TEXT,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # User preferences
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS preferences (
                user_id INTEGER PRIMARY KEY,
                language TEXT DEFAULT 'uz',
                timezone TEXT DEFAULT 'Asia/Tashkent',
                notifications BOOLEAN DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        conn.commit()
        print("Database initialized successfully")

def save_user_tokens(user_id: int, tokens: Dict):
    """Save user OAuth tokens"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        tokens_json = json.dumps(tokens)
        email = tokens.get('email', '')
        
        cursor.execute('''
            INSERT INTO users (user_id, email, tokens, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(user_id) DO UPDATE SET
                email = excluded.email,
                tokens = excluded.tokens,
                updated_at = CURRENT_TIMESTAMP
        ''', (user_id, email, tokens_json))
        
        conn.commit()

def get_user_tokens(user_id: int) -> Optional[Dict]:
    """Get user OAuth tokens"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute('SELECT tokens FROM users WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        
        if row and row['tokens']:
            return json.loads(row['tokens'])
        
        return None

def delete_user_tokens(user_id: int):
    """Delete user OAuth tokens"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
        cursor.execute('DELETE FROM events WHERE user_id = ?', (user_id,))
        cursor.execute('DELETE FROM notes WHERE user_id = ?', (user_id,))
        cursor.execute('DELETE FROM preferences WHERE user_id = ?', (user_id,))
        
        conn.commit()

def save_event(user_id: int, event_id: str, title: str, start_time: str):
    """Cache event information"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO events (user_id, event_id, title, start_time)
            VALUES (?, ?, ?, ?)
        ''', (user_id, event_id, title, start_time))
        
        conn.commit()

def get_user_events(user_id: int, limit: int = 10) -> list:
    """Get cached user events"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM events
            WHERE user_id = ?
            ORDER BY start_time DESC
            LIMIT ?
        ''', (user_id, limit))
        
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def save_note(user_id: int, note_id: str, title: str, content: str):
    """Cache note information"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO notes (user_id, note_id, title, content)
            VALUES (?, ?, ?, ?)
        ''', (user_id, note_id, title, content))
        
        conn.commit()

def get_user_notes(user_id: int, limit: int = 10) -> list:
    """Get cached user notes"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM notes
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        ''', (user_id, limit))
        
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def save_user_preference(user_id: int, key: str, value: str):
    """Save user preference"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute(f'''
            INSERT INTO preferences (user_id, {key})
            VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                {key} = excluded.{key}
        ''', (user_id, value))
        
        conn.commit()

def get_user_preferences(user_id: int) -> Optional[Dict]:
    """Get user preferences"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM preferences WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        
        if row:
            return dict(row)
        
        return None

def get_all_users() -> list:
    """Get all registered users"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute('SELECT user_id, email FROM users')
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]

# Database maintenance
def cleanup_old_cache(days: int = 30):
    """Clean up old cached events and notes"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM events
            WHERE created_at < datetime('now', '-' || ? || ' days')
        ''', (days,))
        
        cursor.execute('''
            DELETE FROM notes
            WHERE created_at < datetime('now', '-' || ? || ' days')
        ''', (days,))
        
        conn.commit()
        print(f"Cleaned up cache older than {days} days")

if __name__ == '__main__':
    # Initialize database
    init_db()
    print("Database setup complete!")