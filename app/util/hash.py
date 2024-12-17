from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hash the password
    :param password: password to hash
    :return: hashed password
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify the password
    :param plain_password: original password
    :param hashed_password: hashed password
    :return: True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)