import jwt
from jwt.exceptions import InvalidSignatureError

from typing import Union, Annotated
from datetime import datetime, timedelta, timezone

from fastapi import status, HTTPException
from fastapi import Depends

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from passlib.context import CryptContext

from app.config import auth_settings

from app.user.models import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_JWT_token(data: dict, is_refresh: bool = False):
    to_encode = data.copy()

    expires_in_seconds = int(auth_settings.JWT_EXPIRES)
    if is_refresh:
        expires_in_seconds = int(auth_settings.JWT_REFRESH_EXPIRES)

    expire_date = datetime.now(timezone.utc) + timedelta(seconds=expires_in_seconds)
    to_encode.update({ 'exp': expire_date, 'is_refresh': is_refresh })

    encoded_jwt = jwt.encode(to_encode, auth_settings.JWT_SECRET, algorithm=auth_settings.JWT_ALGORITHM)
    return encoded_jwt, expires_in_seconds

def decode_jwt_token(token: str, is_refresh: bool = False):
    ''' returns jwt payload '''
    try:
        payload = jwt.decode(token, auth_settings.JWT_SECRET, algorithms=[auth_settings.JWT_ALGORITHM])
    except InvalidSignatureError as e:
        print('InvalidSignatureError')
        return None

    if is_refresh and not payload['is_refresh']:
        return None

    return payload

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password, hashed_password: str):
    return pwd_context.verify(password, hashed_password)
