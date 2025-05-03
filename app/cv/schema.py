from typing import List

from pydantic import BaseModel

from .project.schema import CVProjectBase, CVProjectPublic
from app.user.schema import UserBase, UserProfile


class CVBase(BaseModel):
    id: int
    user: UserBase
    about: str


class CVDetail(CVBase):
    projects: List[CVProjectBase]


class CVDetailPublic(CVBase):
    user: UserProfile # override
    projects: List[CVProjectPublic]


class CVList(BaseModel):
    id: int
    about: str


class CreateCVBase(BaseModel):
    about: str


class CreateCVBaseWithPosition(CreateCVBase):
    position: int
