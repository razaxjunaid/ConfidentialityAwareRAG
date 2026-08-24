import sqlite3
from pathlib import Path

DB_PATH = Path("data/database.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def get_connection():
    """Create and return a SQLite database connection."""
    return sqlite3.connect(str(DB_PATH))


def create_users_table(cursor):
    """Create the users table."""
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL,
        status INTEGER DEFAULT 1
    );
    """)


def create_documents_table(cursor):
    """Create the documents table."""
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        classification TEXT NOT NULL,
        version INTEGER DEFAULT 1,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)


def create_tables():
    """Create all required database tables."""
    conn = get_connection()
    cursor = conn.cursor()

    create_users_table(cursor)
    create_documents_table(cursor)

    conn.commit()
    conn.close()


def initialize_database():
    """Create tables and seed default users."""
    create_tables()

    from database.db import seed_users
    seed_users()


if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully!")