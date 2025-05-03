from typing import List

from pydantic import BaseModel

from .project.schema import CVProjectBase
from app.user.schema import UserBase, UserProfile


class CVBase(BaseModel):
    id: int
    user: UserBase
    about: str


class CVDetail(CVBase):
    projects: List[CVProjectBase]


class CVDetailPublic(CVBase):
    user: UserProfile # override
    projects: List[CVProjectBase]


class CVList(BaseModel):
    id: int
    about: str


class CreateCVBase(BaseModel):
    about: str


class CreateCVBaseWithPosition(CreateCVBase):
    position: int
