import logging

from typing import List, Annotated

from fastapi import APIRouter, HTTPException, status
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database.core import get_db

from .manager import UserManager, get_user_manager
from app.auth.manager import get_current_user

from .models import User
from .schema import UsersDevInfo
from .schema import UserBase, UserProfile, UpdateUserBase


log = logging.getLogger(__name__)

user_router = APIRouter(prefix='/users')

# DEV Section

'''
@user_router.get('/dev-info-old')
async def users_list(db: Session = Depends(get_db)):
    users = get_users(db)
    return {
        'users': users,
    }

'''

# TODO: UserManagerType
@user_router.get('/dev-info')
async def dev_users_list(user_manager: UserManager = Depends(get_user_manager)):
    users = user_manager.get_users()
    print('uuuusers: ', users)
    return {
        'users': users,
    }


@user_router.get('/{user_id}')
async def get_user(user_id: int, user_manager = Depends(get_user_manager)) -> UserProfile:
    db_user = user_manager.get_user_by_id(user_id)
    if not db_user:
        raise HTTPException(404, f'User doesnt exists')

    return db_user

@user_router.put('/{user_id}')
async def update_user_profile(
    *,
    user_id: int,
    userProfileData: UpdateUserBase,
    user_manager = Depends(get_user_manager),
    current_user: Annotated[User, Depends(get_current_user)]
) -> UserProfile:
    if current_user.id != user_id:
        raise HTTPException(405, f'Method Not Allowed')

    user = user_manager.get_user_by_id(user_id)
    if not user:
        raise HTTPException(404, f'User does not exists')

    updated_user = user_manager.update_user(user, userProfileData)
    if not updated_user:
        raise HTTPException(500, f'User does not updated')

    return updated_user




#
