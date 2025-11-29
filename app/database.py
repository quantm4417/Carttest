import sqlite3
import json
from datetime import datetime
from app.config import Config
from app.models import create_tables

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with tables"""
    create_tables()

def log_message(level, message, context=None):
    """Log a message to the database"""
    conn = get_db()
    try:
        conn.execute(
            'INSERT INTO logs (timestamp, level, message, context) VALUES (?, ?, ?, ?)',
            (datetime.utcnow().isoformat(), level, message, json.dumps(context) if context else None)
        )
        conn.commit()
    except Exception as e:
        print(f"Error logging message: {e}")
    finally:
        conn.close()



