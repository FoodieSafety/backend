import jwt
from dotenv import load_dotenv
import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from datetime import datetime, timedelta, timezone
from app.util.schemas import TokenData

# Load environment variables
load_dotenv()

# pass in the same url as the one in the login route
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(source_data: dict, expire_delta: timedelta = None):
    """
    Create an access JWT token
    :param source_data: input payload from the client
    :return: encrypted JWT token
    :param expire_delta: time delta for expiration
    :return: encoded JWT token
    """

    # Make a copy of the source data
    to_encode = source_data.copy()

    # Calculate the expiration time
    if expire_delta:
        expire_time = datetime.now(timezone.utc) + expire_delta
    else:
        expire_time = datetime.now(timezone.utc) + timedelta(minutes=int(os.getenv("EXPIRE_TIME")))

    # Update the payload with the expiration time
    to_encode.update({"exp": expire_time})

    # Create the JWT token
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))

    return encoded_jwt


def validate_access_token(token: str, credential_exception):
    try:
        # Decode the token
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=os.getenv("ALGORITHM"))

        # Check if the payload contains the required fields
        user_id = payload.get("sub")
        if not user_id:
            raise credential_exception

        token_data = TokenData(user_id=user_id)

    except jwt.exceptions.InvalidTokenError:
        raise credential_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    return validate_access_token(token, exception)






