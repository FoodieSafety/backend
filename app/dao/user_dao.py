from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List
from fastapi import HTTPException, status
from app.util.schemas import UserCreate, UserResponse
from app.util.models import Base, User
from app.util.database import engine
from app.util.hash import hash_password

# Bind engine to metadata and create all tables
Base.metadata.create_all(bind=engine)

class UserDao:
    """
    Talk to the database and perform CRUD operations on User object
    and return the response to the controller
    """
    @staticmethod
    def create_user(user: UserCreate, db: Session) -> UserResponse:
        """
        Create a new user in the database
        :param user: user details
        :param db: Session object
        :return: response
        """
        # Check duplication in username or email
        existing_user = db.query(User).filter(
            or_(
                User.username == user.username,
                User.email == user.email
            )
        ).first()

        if existing_user:
            if existing_user.username == user.username:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
            if existing_user.email == user.email:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

        # Hash password and store it back
        user.password = hash_password(user.password)

        # valid user, create
        new_user = User(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return UserResponse(**new_user.__dict__)


    @staticmethod
    def get_users(db: Session) -> List[UserResponse]:
        """
        Get all users from the database
        :return: all users
        """
        users = db.query(User).all()
        return [UserResponse(**user.__dict__) for user in users]


    @staticmethod
    def get_user_by_id(user_id: int, db: Session) -> UserResponse:
        """
        Get user by ID
        :param user_id: user ID
        :param db: Session object
        :return: user details
        """
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found")
        return UserResponse(**user.__dict__)