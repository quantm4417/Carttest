import json
import sqlite3
from datetime import datetime
from app.config import Config

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_product_by_id(product_id):
    """Get product by ID"""
    conn = get_db()
    try:
        row = conn.execute(
            'SELECT * FROM products WHERE id = ?', (product_id,)
        ).fetchone()
        if row:
            product = dict(row)
            if product.get('options'):
                product['options'] = json.loads(product['options'])
            return product
        return None
    finally:
        conn.close()

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
