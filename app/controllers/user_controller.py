from sqlalchemy.orm import Session
from typing import List
from app.util.schemas import UserCreate, UserResponse
from app.dao.user_dao import UserDao


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
    def update_user(user_id: int, user: UserCreate, db: Session) -> UserResponse:
        pass
