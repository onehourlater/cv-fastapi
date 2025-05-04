from fastapi import Depends

from app.database.core import get_db, Session

from .models import User
from app.auth.schema import UserBaseAuth
from .schema import UserProfile
from .schema import CreateUserBase, UpdateUserBase, UpdateUserProfile
from .service import get_all_users, get_all_users_count
from .service import get_user_by_id, get_user_by_email, get_user_by_username
from .service import create_user, update_user, update_user_profile, update_user_password
from .service import generate_username
from .service import is_user_exists


class UserManager:
    def __init__(self, db: Session):
        print()
        print('[UserManager] __init__')
        self.db = db

    # Commons

    def get_users(self) -> UserProfile:
        return get_all_users(self.db)

    def get_users_count(self) -> int:
        return get_all_users_count(self.db)

    def is_user_already_exists(self, auth_data: UserBaseAuth) -> bool:
        return is_user_exists(self.db, auth_data)

    # Get

    def get_user_by_id(self, user_id: int) -> User:
        return get_user_by_id(self.db, user_id)

    def get_user_by_email(self, user_email: str) -> User:
        return get_user_by_email(self.db, user_email)

    def get_user_by_username(self, username: str) -> User:
        return get_user_by_username(self.db, username)

    def create_user(self, data: CreateUserBase) -> User:
        new_user = create_user(self.db, data)
        username = generate_username(self.db, new_user)
        new_user = update_user(self.db, new_user, UpdateUserBase(username=username))

        return new_user

    def change_user_password(self, user: User, user_password_hash: str):
        update_user_password(self.db, user, user_password_hash)

    def update_user(self, user: User, user_profile: UpdateUserProfile) -> User:
        print()
        print('[update_user] user_profile: ', user_profile)
        return update_user_profile(self.db, user, user_profile)



def get_user_manager(db: Session = Depends(get_db)) -> UserManager:
    return UserManager(db)


#
