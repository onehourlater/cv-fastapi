from typing import List, Annotated, Union

from passlib.context import CryptContext

from fastapi import Depends
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.config import auth_settings
from app.database.core import get_db
from app.exceptions import ExistsError, NotExistsError, WrongCredentials

from app.user.schema import CreateUserBase
from app.user.models import User
from app.user.manager import UserManager, get_user_manager

from .schema import UserBaseAuth
from .utils import verify_password, get_password_hash
from .utils import create_JWT_token, decode_jwt_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='')

class AuthManager:
    def __init__(self, db: Session, user_manager: UserManager):
        self.db = db
        self.user_manager = user_manager

    def signup(self, auth_data: UserBaseAuth) -> User:
        if self.user_manager.is_user_already_exists(auth_data):
            raise ExistsError('User already exists')

        user_password_hashed = get_password_hash(auth_data.password)

        try:
            new_user = self.user_manager.create_user(CreateUserBase(
                email=auth_data.email,
                password=user_password_hashed
            ))
        except Exception as e:
            print(f'self.user_manager.create_user ERROR {e}')
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )

        return new_user

    def authenticate(self, auth_data: UserBaseAuth) -> User:
        user = self.user_manager.get_user_by_email(auth_data.email)
        if not user:
            print('raise NotExistsError')
            raise NotExistsError('User with provided email does not exists')
        if not verify_password(auth_data.password, user.password):
            print('raise WrongCredentials')
            raise WrongCredentials('Invalid credentials')

        return user

    def change_password(self, user: User, password: str) -> User:
        user_password_hashed = get_password_hash(password)

        user.password = user_password_hashed
        self.db.commit()

        return user

    # no tests
    def get_user_by_token(self, token: str) -> Union[User, None]:
        try:
            payload = decode_jwt_token(token)
            username = payload.get(auth_settings.JWT_USERNAME_KEY)
            if username is None:
                return None

        except Exception as e:
            print('get_current_user e: ', e)
            return None

        user = self.user_manager.get_user_by_username(username)
        if user is None:
            return None

        return user

def get_auth_manager(db: Session = Depends(get_db), user_manager = Depends(get_user_manager)) -> AuthManager:
    print()
    print('[get_auth_manager]')
    return AuthManager(db, user_manager)

def get_current_user(*, token: Annotated[str, Depends(oauth2_scheme)], auth_manager = Depends(get_auth_manager)) -> User:
    user = auth_manager.get_user_by_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
