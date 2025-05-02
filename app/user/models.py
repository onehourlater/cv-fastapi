from typing import Optional, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database.core import Base


def get_default_username(context):
    params = context.get_current_parameters()
    user_email = params['email']
    return f'{user_email}'


class UserBase(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True, default=get_default_username)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(deferred=True)


class User(UserBase):
    __tablename__ = 'user_table'

    full_name: Mapped[Optional[str]] = mapped_column(String(150), default='')
    kind_of_activity: Mapped[Optional[str]] = mapped_column(String(150), default='')
    about: Mapped[Optional[str]] = mapped_column(default='')
    # picture: Mapped[str] =

    cvs: Mapped[List['CV']] = relationship(back_populates='user')

    def __repr__(self):
        return f'{self.id}. {self.username}'
