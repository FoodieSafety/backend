from sqlalchemy.orm import Session
from typing import List
from ..util.schemas import UserCreate, UserResponse, TokenData
from ..dao.user_dao import UserDao


class UserController:
    """
    Controller for CRUD operations on User object
    and passing response from model to view
    """
    @staticmethod
    def create_user(user: UserCreate, db: Session) -> UserResponse:
        return UserDao.create_user(user, db)


    @staticmethod
    def get_users(db: Session) -> List[UserResponse]:
        return UserDao.get_users(db)

    @staticmethod
    def get_user_by_id(user_id: int, db: Session) -> UserResponse:
        return UserDao.get_user_by_id(user_id, db)

    @staticmethod
    def update_user(user: UserCreate, db: Session, token_data: TokenData) -> UserResponse:
        # Get the user id from the token
        user_id = token_data.user_id
        return UserDao.update_user(user, db, user_id)

    @staticmethod
    def delete_user(db: Session, token_data: TokenData) -> None:
        # Get the user id from the token
        user_id = token_data.user_id
        return UserDao.delete_user(db, user_id)