import logging

from typing import List, Annotated

from fastapi import APIRouter, HTTPException, status
from fastapi import Body, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.config import auth_settings
from app.database.core import get_db
from app.exceptions import ExistsError, NotExistsError, WrongCredentials

from app.user.models import User
from app.user.manager import get_user_manager
from .manager import get_auth_manager, get_current_user

from .schema import UserBase, UserBaseAuth, UserBaseAuth
from .schema import AuthTokens, AccessToken
from .utils import create_JWT_token


log = logging.getLogger(__name__)

auth_router = APIRouter()


@auth_router.post('/signup')
async def signup(auth_data: UserBaseAuth, auth_manager = Depends(get_auth_manager)) -> UserBase:
    print()
    print('[signup] auth_manager: ', auth_manager)
    try:
        new_user = auth_manager.signup(auth_data)
    except ExistsError as e:
        log.warning(f'User already exists: {str(auth_data)}')
        raise HTTPException(400, str(e))
    except Exception as e:
        log.error(f'error occured on auth_router /signup handler {e}')
        raise HTTPException(500, f'Error occured')

    return new_user

@auth_router.post('/signin')
async def signin(auth_data: UserBaseAuth, auth_manager = Depends(get_auth_manager)) -> AuthTokens:
    try:
        user = auth_manager.authenticate(auth_data)
    except NotExistsError as e:
        print('not exists 400')
        raise HTTPException(400, str(e))
    except WrongCredentials as e:
        print('not exists 401')
        raise HTTPException(401, str(e))
    except Exception as e:
        print(f'signin 500 {e}')
        log.error(f'error occured on auth_router /signin handler {e}')
        raise HTTPException(500, f'Error occured')

    access_token, access_token_expires = create_JWT_token(
        data={ auth_settings.JWT_USERNAME_KEY: user.username }
    )
    refresh_token, refresh_token_expires = create_JWT_token(
        data={ auth_settings.JWT_USERNAME_KEY: user.username },
        is_refresh=True
    )
    return AuthTokens(
        token_type='bearer',
        access_token=access_token, access_expires_seconds=access_token_expires,
        refresh_token=refresh_token, refresh_expires_seconds=refresh_token_expires
    )


@auth_router.post('/password')
async def change_password(password: Annotated[str, Body(embed=True)], current_user: Annotated[User, Depends(get_current_user)], auth_manager = Depends(get_auth_manager)):
    auth_manager.change_password(current_user, password)

    return {
        'password': password
    }


@auth_router.post('/auth/refresh')
async def auth_refresh(refresh_token: Annotated[str, Body(embed=True)], user_manager = Depends(get_user_manager)) -> AccessToken:
    ''' Takes refresh token and response with new access token '''
    jwt_payload = decode_jwt_token(refresh_token, is_refresh=True)
    if not jwt_payload:
        raise HTTPException(401, 'Could not validate credentials')

    jwt_payload_username = jwt_payload.get(auth_settings.JWT_USERNAME_KEY)
    if not jwt_payload_username:
        raise HTTPException(401, 'Could not validate credentials')

    user = user_manager.get_user_by_username(username=jwt_payload_username)

    access_token, access_token_expires = create_JWT_token(
        data={ auth_settings.JWT_USERNAME_KEY: user.username }
    )

    return AccessToken(
        token_type='bearer',
        access_token=access_token, access_expires_seconds=access_token_expires
    )

@auth_router.get('/me')
async def get_me(current_user: Annotated[User, Depends(get_current_user)]) -> UserBase:
    return current_user

#
