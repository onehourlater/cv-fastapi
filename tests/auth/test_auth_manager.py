import pytest

from sqlalchemy import select
from sqlalchemy.orm import Session

from tests.constants import TestConstants

from app.exceptions import ExistsError, NotExistsError, WrongCredentials

from app.user.models import User
from app.user.schema import CreateUserBase
from app.user.manager import UserManager

from app.auth.schema import UserBaseAuth
from app.auth.manager import AuthManager
from app.auth.utils import verify_password, get_password_hash


# @pytest.mark.usefixtures('client')
class TestAuthManager:
    DEFAULT_EMAIL = 'hello@gmail.com'
    DEFAULT_PASSWORD = 'kitty'

    def _get_user_by_email(self, db_session: Session, email: str):
        query = select(User).where(User.email == email)
        return db_session.scalars(query).one_or_none()

    def _create_user_in_db(
        self, user_manager: UserManager, email: str, password: str
    ) -> User:
        hashed_password = get_password_hash(password)
        return user_manager.create_user(
            CreateUserBase(email=email, password=hashed_password)
        )

    #

    def test_auth_manager_signup(self, auth_manager: AuthManager, db_session: Session):
        out_user = auth_manager.signup(
            UserBaseAuth(
                email=TestConstants.USER_EMAIL, password=TestConstants.USER_PASSWORD
            )
        )

        db_user = self._get_user_by_email(db_session, TestConstants.USER_EMAIL)

        assert out_user.email == db_user.email
        assert verify_password(TestConstants.USER_PASSWORD, db_user.password)

    def test_auth_manager_signup_already_exists(
        self, auth_manager: AuthManager, user_manager: UserManager
    ):
        # create user in Database
        self._create_user_in_db(
            user_manager, TestConstants.USER_EMAIL, TestConstants.USER_PASSWORD
        )

        # trying to create user with same credentials
        with pytest.raises(ExistsError):
            auth_manager.signup(
                UserBaseAuth(
                    email=TestConstants.USER_EMAIL, password=TestConstants.USER_PASSWORD
                )
            )

    def test_auth_manager_authenticate(
        self, auth_manager: AuthManager, user_manager: UserManager
    ):
        self._create_user_in_db(
            user_manager, TestConstants.USER_EMAIL, TestConstants.USER_PASSWORD
        )

        user = auth_manager.authenticate(
            UserBaseAuth(
                email=TestConstants.USER_EMAIL, password=TestConstants.USER_PASSWORD
            )
        )
        assert user.email == TestConstants.USER_EMAIL

    def test_auth_manager_authenticate_wrong_credentials(
        self, auth_manager: AuthManager, user_manager: UserManager
    ):
        self._create_user_in_db(
            user_manager, TestConstants.USER_EMAIL, TestConstants.USER_PASSWORD
        )

        with pytest.raises(NotExistsError):
            auth_manager.authenticate(
                UserBaseAuth(email='doesntexist@gmail.com', password='wrongpassword')
            )

        with pytest.raises(WrongCredentials):
            auth_manager.authenticate(
                UserBaseAuth(email=TestConstants.USER_EMAIL, password='wrongpassword')
            )


#
