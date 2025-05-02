from typing import Annotated

from fastapi import Depends

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from app.config import db_settings


POSTGRES_URL = f'postgresql://{db_settings.POSTGRES_USER}:{db_settings.POSTGRES_PASSWORD}@{db_settings.POSTGRES_HOSTNAME}:{db_settings.DATABASE_PORT}/{db_settings.POSTGRES_DB}'

engine = create_engine(POSTGRES_URL, echo=True)
# WHY: что это делает?
# setup_guids_postgresql(engine)

Base = declarative_base()
# WHY: sessionmaker без параметров по умолчанию синхронная?
session_local = sessionmaker(bind=engine)


def drop_create_models():
    with engine.begin() as conn:
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)


def create_models():
    with engine.begin() as conn:
        Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    print()
    print('[get_db]')
    with session_local() as session:
        print('[yield session]')
        yield session


DbSession = Annotated[Session, Depends(get_db)]


#
