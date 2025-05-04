from typing import List

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.auth.schema import UserBaseAuth
from app.user.models import User
from .schema import CreateUserBase, UpdateUserBase, UpdateUserProfile


def get_all_users(db: Session) -> List[User]:
    query = select(User)
    return db.scalars(query).all()

def get_all_users_count(db: Session) -> int:
    query = select(func.count(User.id)).select_from(User)
    return db.scalar(query)

def get_user_by_id(db: Session, user_id: int) -> User:
    return db.get(User, user_id)

def get_user_by_email(db: Session, user_email: str) -> User:
    query = select(User).where(User.email == user_email)
    result = db.scalars(query).one_or_none()
    return result

def get_user_by_username(db: Session, username: str) -> User:
    query = select(User).where(User.username == username)
    result = db.scalars(query).one_or_none()
    return result

def is_user_exists(db: Session, auth_data: UserBaseAuth) -> bool:
    query = (
        select(func.count(User.id))
        .select_from(User)
        .filter(User.email == auth_data.email)
    )
    result = db.scalar(query)
    return True if result else False

def create_user(db: Session, user_data: CreateUserBase) -> User:
    new_user = User(email=user_data.email, password=user_data.password)
    db.add(new_user)
    db.commit()
    return new_user

def update_user(db: Session, user: User, user_data: UpdateUserBase) -> User:
    for key, value in user_data.model_dump().items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user

# TODO: almost same as update_user, updating data scheme is different only
def update_user_profile(db: Session, user: User, user_profile: UpdateUserProfile) -> User:
    print()
    print('[update_user_profile]')
    print('user: ', user)
    print('user.username: ', user.username)
    print('user_profile: ', user_profile)
    for key, value in user_profile.model_dump().items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user

def update_user_password(db: Session, user: User, hashed_password: str):
    user.password = hashed_password
    db.commit()

def generate_username(db: Session, user: User) -> str:
    # default username: {user.email.split('@')[0]}-{user.id}
    # generated username: {user.email.split('@')[0]} i.e. without user.id
    # Returns generated username without id or None
    # Additional check requires in case of hello@gmail.com and hello@mail.ru
    username = user.email.split('@')[0]

    query = (
        select(func.count(User.id))
        .select_from(User)
        .filter(User.username == username)
    )
    users_with_username_count = db.scalar(query)

    if users_with_username_count > 0:
        users_count = get_all_users_count(db)
        return f'{username}-{users_count}'

    return username





#
