import pytest

from typing import Any, Generator

from fastapi import FastAPI
from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from app.config import auth_settings
from app.database.core import Base, get_db
from app.main import get_application

from app.auth.manager import get_auth_manager
from app.user.manager import get_user_manager
from app.user.models import User

from app.auth.utils import create_JWT_token

from .constants import TestConstants
from .factories.user import UserFactory
from .factories.cv import CVFactory


engine = create_engine('sqlite://', connect_args={'check_same_thread': False})

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

"""
user_manager = get_user_manager(Session)
auth_manager = get_auth_manager(Session, user_manager)

print('')
print('[CONFTEST]')
print('user_manager: ', user_manager)
"""


@pytest.fixture(autouse=True)
def app() -> Generator[FastAPI, Any, None]:
    Base.metadata.create_all(engine)  # Create the tables.
    _app = get_application()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session(app: FastAPI) -> Generator[Session, Any, None]:
    """
    Creates a fresh sqlalchemy session for each test that operates in a
    transaction. The transaction is rolled back at the end of each test ensuring
    a clean state.
    """

    # connect to the database
    connection = engine.connect()
    # begin a non-ORM transaction
    transaction = connection.begin()
    # bind an individual Session to the connection
    session = Session(bind=connection)
    yield session  # use the session in tests.
    session.close()
    # rollback - everything that happened with the
    # Session above (including calls to commit())
    # is rolled back.
    transaction.rollback()
    # return connection to the Engine
    connection.close()


@pytest.fixture()
def user_manager(db_session: Session):
    yield get_user_manager(db_session)


@pytest.fixture()
def auth_manager(user_manager):
    yield get_auth_manager(user_manager)


@pytest.fixture(autouse=True)
def set_session_for_factories(db_session: Session):
    UserFactory._meta.sqlalchemy_session = db_session
    CVFactory._meta.sqlalchemy_session = db_session


def get_or_create_default_user(db_session: Session) -> User:
    user = db_session.scalars(
        select(User).where(User.email == TestConstants.USER_EMAIL)
    ).one_or_none()
    print()
    print('get_or_create_default_user')
    print('user: ', user)

    if user:
        return user

    return UserFactory(email=TestConstants.USER_EMAIL)


@pytest.fixture()
def default_user(
    client: TestClient, db_session: Session
) -> Generator[TestClient, Any, None]:
    yield get_or_create_default_user(db_session)


@pytest.fixture()
def authenticated_client(
    client: TestClient, db_session: Session
) -> Generator[TestClient, Any, None]:
    default_user: User = get_or_create_default_user(db_session)
    access_token, access_token_inspiration = create_JWT_token(
        {auth_settings.JWT_USERNAME_KEY: default_user.username}
    )
    headers = {'Authorization': f'Bearer {access_token}'}
    client.headers.update(headers)
    yield client
    client.headers.clear()


@pytest.fixture()
def client(app: FastAPI, db_session: Session) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client
