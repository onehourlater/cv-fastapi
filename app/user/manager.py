from typing import List, Annotated

from passlib.context import CryptContext

from fastapi import Depends
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.config import auth_settings
from app.database.core import get_db

from .models import User
from app.auth.schema import UserBaseAuth
from .schema import UserProfile
from .schema import CreateUserBase, UpdateUserBase


class UserManager:
    def __init__(self, db: Session):
        print()
        print('[UserManager] __init__')
        self.db = db

    # Commons

    def get_users(self) -> UserProfile:
        query = select(User)
        result = self.db.scalars(query).all()
        return result

    def get_users_count(self) -> int:
        query = select(func.count(User.id)).select_from(User)
        users_count = self.db.scalar(query)
        return users_count

    def is_user_already_exists(self, auth_data: UserBaseAuth) -> bool:
        query = select(func.count(User.id)).select_from(User).filter(User.email==auth_data.email)
        result = self.db.scalar(query)

        return True if result else False

    # Get

    def get_user_by_id(self, id: int) -> User:
        return self.db.get(User, id)

    def get_user_by_email(self, email: str) -> User:
        query = select(User).where(User.email==email)
        result = self.db.scalars(query).one_or_none()
        return result

    def get_user_by_username(self, username: str) -> User:
        query = select(User).where(User.username==username)
        result = self.db.scalars(query).one_or_none()
        return result

    # Create

    def create_user(self, data: CreateUserBase) -> User:
        new_user = User(email=data.email, password=data.password)
        self.db.add(new_user)
        self.db.flush()

        new_user.username = self.generate_username(new_user)

        self.db.commit()
        return new_user

    # Update

    def update_user(self, user: User, userProfile: UpdateUserBase) -> User:
        for key, value in userProfile.model_dump().items():
            setattr(user, key, value)

        self.db.commit()
        self.db.refresh(user)

        return user

    # Helpers

    def generate_username(self, user: User) -> str:
        # default username: {user.email.split('@')[0]}-{user.id}
        # generated username: {user.email.split('@')[0]} i.e. without user.id
        # Returns generated username without id or None
        # Additional check requires in case of hello@gmail.com and hello@mail.ru
        username = user.email.split('@')[0]

        query = select(func.count(User.id)).select_from(User).filter(User.username==username)
        users_with_username_count = self.db.scalar(query)

        if users_with_username_count > 0:
            users_count = self.get_users_count()
            return f'{username}-{users_count}'

        return username


def get_user_manager(db: Session = Depends(get_db)) -> UserManager:
    return UserManager(db)



#
