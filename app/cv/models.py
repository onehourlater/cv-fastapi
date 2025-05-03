from typing import TYPE_CHECKING
from datetime import datetime

from typing import Optional, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database.core import Base


# in case ruff: User is undefined
if TYPE_CHECKING:
    from app.user.models import User

# projects - link to projects
# work experience
# education
# contacts

class CV(Base):
    __tablename__ = 'cv_table'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_table.id'))
    user: Mapped['User'] = relationship(back_populates='cvs')

    about: Mapped[Optional[str]] = mapped_column(default='')

    position: Mapped[int]

    projects: Mapped[List['CVProject']] = relationship(back_populates='cv')

    def __repr__(self):
        return f'CV: {self.id}'


class CVProject(Base):
    __tablename__ = 'cv_project_table'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cv_id: Mapped[int] = mapped_column(ForeignKey('cv_table.id'))
    cv: Mapped['CV'] = relationship(back_populates='projects')

    title: Mapped[str]
    client: Mapped[Optional[str]] = mapped_column(default='')

    end_date: Mapped[datetime]
    is_ongoing: Mapped[Optional[bool]] = mapped_column(default=False)

    link: Mapped[Optional[str]] = mapped_column(default='')

    description: Mapped[Optional[str]] = mapped_column(default='')

    position: Mapped[int]

    def __repr__(self):
        return f'CV Project: {self.id}'
