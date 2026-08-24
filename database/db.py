import sqlite3
from pathlib import Path


DB_PATH = Path("data/database.db")


def get_connection():
    """
    Create and return a database connection.
    """

    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row

    return conn


def add_user(username, password_hash, role):
    """
    Add a new user to the database.
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users(
                username,
                password_hash,
                role
            )
            VALUES (?, ?, ?)
            """,
            (username, password_hash, role)
        )

        conn.commit()

        print(f"User '{username}' added successfully.")

    except sqlite3.IntegrityError:

        print(f"User '{username}' already exists.")

    finally:

        conn.close()


def get_user_by_username(username):
    """
    Return user details by username.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM users
        WHERE username = ?
        """,
        (username,)
    )

    user = cursor.fetchone()

    conn.close()

    return user


def get_all_users():
    """
    Return all users.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users"
    )

    users = cursor.fetchall()

    conn.close()

    return users


def seed_users():
    """
    Insert default users.
    """

    from auth.password import hash_password

    users = [
        ("viewer", hash_password("viewer123"), "viewer"),
        ("staff", hash_password("staff123"), "staff"),
        ("senior", hash_password("senior123"), "senior"),
        ("executive", hash_password("executive123"), "executive")
    ]

    for username, password_hash, role in users:

        add_user(
            username,
            password_hash,
            role
        )


if __name__ == "__main__":

    seed_users()

    print("\nUsers in Database:\n")

    users = get_all_users()

    for user in users:
        print(dict(user))