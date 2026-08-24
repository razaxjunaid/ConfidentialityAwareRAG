from database.db import get_user_by_username
from auth.password import verify_password


def login(username: str, password: str):
    """
    Authenticate a user using username and password.

    Returns user information if successful.
    Returns None if authentication fails.
    """

    # Get user from database
    user = get_user_by_username(username)

    # User does not exist
    if user is None:
        return None

    # Verify password
    if not verify_password(
        password,
        user["password_hash"]
    ):
        return None

    # Login successful
    return {
        "id": user["id"],
        "username": user["username"],
        "role": user["role"]
    }


if __name__ == "__main__":

    print("\n========== LOGIN TEST ==========\n")

    username = input("Username: ")
    password = input("Password: ")

    user = login(username, password)

    if user:

        print("\n✅ Login Successful!")

        print(f"\nUsername : {user['username']}")
        print(f"Role     : {user['role']}")

    else:

        print("\n❌ Invalid username or password.")