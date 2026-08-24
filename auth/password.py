from passlib.context import CryptContext

# Password hashing configuration
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    """
    Convert plain password into a secure hash.
    """
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify whether the entered password matches the stored hash.
    """
    return pwd_context.verify(password, hashed_password)


if __name__ == "__main__":

    password = "viewer123"

    hashed = hash_password(password)

    print("Original :", password)
    print("Hash     :", hashed)

    print("Verify :", verify_password(password, hashed))