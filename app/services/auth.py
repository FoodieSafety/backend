from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..util.database import get_db
from ..util.schemas import UserLogin
from ..util.models import User
from ..util.hash import verify_password
from ..util.oauth2 import create_access_token
router = APIRouter(tags=["Authentication"])

@router.post("/login", status_code=status.HTTP_200_OK)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    User login
    :param user_credentials: user credentials to login
    :param db: session object
    :return: response
    """
    # Check valid username
    user = db.query(User).filter(
        User.username == user_credentials.username,
    ).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login credentials")

    # Check password
    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login credentials")

    # Create JWT token
    access_token = create_access_token(source_data={"user_id": user.user_id})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }