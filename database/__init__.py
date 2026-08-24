import sqlite3
from pathlib import Path

# Path to SQLite database
DB_PATH = Path("data/database.db")

# Create data folder if it doesn't exist
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def get_connection():
    """
    Create and return a SQLite database connection.
    """
    return sqlite3.connect(DB_PATH)

if __name__ == "__main__":
    conn = get_connection()
    print("Database connected successfully!")
    conn.close()