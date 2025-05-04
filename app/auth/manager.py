from typing import Annotated, Union

from fastapi import Depends
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.config import auth_settings
from app.exceptions import ExistsError, NotExistsError, WrongCredentials

from app.user.schema import CreateUserBase
from app.user.models import User
from app.user.manager import UserManager, get_user_manager

from .schema import UserBaseAuth
from .utils import verify_password, get_password_hash
from .utils import decode_jwt_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='', auto_error=False)


class AuthManager:
    def __init__(self, user_manager: UserManager):
        self.user_manager = user_manager

    def signup(self, auth_data: UserBaseAuth) -> User:
        if self.user_manager.is_user_already_exists(auth_data):
            raise ExistsError('User already exists')

        user_password_hashed = get_password_hash(auth_data.password)

        try:
            new_user = self.user_manager.create_user(
                CreateUserBase(email=auth_data.email, password=user_password_hashed)
            )
        except Exception as e:
            print(f'self.user_manager.create_user ERROR {e}')
            raise HTTPException(status_code=500, detail=str(e))

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
        self.user_manager.change_user_password(user, user_password_hashed)
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


def get_auth_manager(
    user_manager=Depends(get_user_manager)
) -> AuthManager:
    return AuthManager(user_manager)

def get_current_user(required: bool = True):
    async def _get_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        auth_manager: Annotated[AuthManager, Depends(get_auth_manager)],
    ) -> User:
        user = auth_manager.get_user_by_token(token)
        if required and not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Could not validate credentials',
                headers={'WWW-Authenticate': 'Bearer'},
            )

        return user

    return _get_user
