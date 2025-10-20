import os
import json
import psycopg
from typing import Dict, Optional
from contextlib import contextmanager

DB_URL = os.getenv('DB_PATH')

@contextmanager
def get_db_connection():
    """Context manager for PostgreSQL connections"""
    with psycopg.connect(DB_URL, sslmode="require") as conn:
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e

def init_db():
    """Initialize database tables"""
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id BIGINT PRIMARY KEY,
                    email TEXT,
                    tokens JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS events (
                    id SERIAL PRIMARY KEY,
                    user_id BIGINT,
                    event_id TEXT,
                    title TEXT,
                    start_time TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS notes (
                    id SERIAL PRIMARY KEY,
                    user_id BIGINT,
                    note_id TEXT,
                    title TEXT,
                    content TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS preferences (
                    user_id BIGINT PRIMARY KEY,
                    language TEXT DEFAULT 'uz',
                    timezone TEXT DEFAULT 'Asia/Tashkent',
                    notifications BOOLEAN DEFAULT TRUE,
                    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
                )
            ''')

            print("Database initialized successfully")

def save_user_tokens(user_id: int, tokens: Dict):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            email = tokens.get('email', '')
            tokens_json = json.dumps(tokens)
            cursor.execute('''
                INSERT INTO users (user_id, email, tokens, updated_at)
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (user_id) DO UPDATE SET
                    email = EXCLUDED.email,
                    tokens = EXCLUDED.tokens,
                    updated_at = CURRENT_TIMESTAMP
            ''', (user_id, email, tokens_json))

def get_user_tokens(user_id: int) -> Optional[Dict]:
    with get_db_connection() as conn:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cursor:
            cursor.execute('SELECT tokens FROM users WHERE user_id = %s', (user_id,))
            row = cursor.fetchone()
            if row and row['tokens']:
                return row['tokens'] if isinstance(row['tokens'], dict) else json.loads(row['tokens'])
            return None

def delete_user_tokens(user_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('DELETE FROM preferences WHERE user_id = %s', (user_id,))
            cursor.execute('DELETE FROM notes WHERE user_id = %s', (user_id,))
            cursor.execute('DELETE FROM events WHERE user_id = %s', (user_id,))
            cursor.execute('DELETE FROM users WHERE user_id = %s', (user_id,))

def save_event(user_id: int, event_id: str, title: str, start_time: str):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                INSERT INTO events (user_id, event_id, title, start_time)
                VALUES (%s, %s, %s, %s)
            ''', (user_id, event_id, title, start_time))

def get_user_events(user_id: int, limit: int = 10) -> list:
    with get_db_connection() as conn:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cursor:
            cursor.execute('''
                SELECT * FROM events
                WHERE user_id = %s
                ORDER BY start_time DESC
                LIMIT %s
            ''', (user_id, limit))
            return cursor.fetchall()

def save_note(user_id: int, note_id: str, title: str, content: str):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                INSERT INTO notes (user_id, note_id, title, content)
                VALUES (%s, %s, %s, %s)
            ''', (user_id, note_id, title, content))

def get_user_notes(user_id: int, limit: int = 10) -> list:
    with get_db_connection() as conn:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cursor:
            cursor.execute('''
                SELECT * FROM notes
                WHERE user_id = %s
                ORDER BY created_at DESC
                LIMIT %s
            ''', (user_id, limit))
            return cursor.fetchall()

def save_user_preference(user_id: int, key: str, value: str):
    allowed_keys = {'language', 'timezone', 'notifications'}
    if key not in allowed_keys:
        raise ValueError(f"Invalid preference key: {key}")

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(f'''
                INSERT INTO preferences (user_id, {key})
                VALUES (%s, %s)
                ON CONFLICT (user_id) DO UPDATE SET {key} = EXCLUDED.{key}
            ''', (user_id, value))

def get_user_preferences(user_id: int) -> Optional[Dict]:
    with get_db_connection() as conn:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cursor:
            cursor.execute('SELECT * FROM preferences WHERE user_id = %s', (user_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

def get_all_users() -> list:
    with get_db_connection() as conn:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cursor:
            cursor.execute('SELECT user_id, email FROM users')
            return cursor.fetchall()

def cleanup_old_cache(days: int = 30):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                DELETE FROM events WHERE created_at < NOW() - INTERVAL '%s days'
            ''', (days,))
            cursor.execute('''
                DELETE FROM notes WHERE created_at < NOW() - INTERVAL '%s days'
            ''', (days,))
            print(f"Cleaned up cache older than {days} days")

if __name__ == '__main__':
    init_db()
    print("Database setup complete!")
