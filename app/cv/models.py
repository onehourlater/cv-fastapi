import enum

from typing import TYPE_CHECKING
from datetime import datetime

from typing import Optional, List

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database.core import Base


# in case ruff: User is undefined
if TYPE_CHECKING:
    from app.user.models import User

# projects - link to projects
# work experience
# education
# contacts

class PublicStatus(enum.Enum):
    PUBLIC      = 2
    LINK_ACCESS = 1
    PRIVATE     = 0


class CV(Base):
    __tablename__ = 'cv_table'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(unique=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('user_table.id'))
    user: Mapped['User'] = relationship(back_populates='cvs')

    about: Mapped[Optional[str]] = mapped_column(default='')

    position: Mapped[int]
    public_status: Mapped[PublicStatus] = mapped_column(default=PublicStatus.PRIVATE)

    projects: Mapped[List['CVProject']] = relationship(back_populates='cv')

    def __repr__(self):
        return f'CV: {self.id}'


class CVProject(Base):
    __tablename__ = 'cv_project_table'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cv_id: Mapped[int] = mapped_column(ForeignKey('cv_table.id'))
    cv: Mapped['CV'] = relationship(back_populates='projects')

    title: Mapped[str]
    role: Mapped[Optional[str]] = mapped_column(default='')

    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    is_ongoing: Mapped[Optional[bool]] = mapped_column(default=False)

    link: Mapped[Optional[str]] = mapped_column(default='')

    description: Mapped[Optional[str]] = mapped_column(default='')

    position: Mapped[int]

    def __repr__(self):
        return f'CV Project: {self.id}'
