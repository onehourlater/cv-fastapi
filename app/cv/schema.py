from typing import List, Optional

from pydantic import BaseModel

from .project.schema import CVProjectBase, CVProjectPublic
from app.user.schema import UserBase, UserProfile


class CVBase(BaseModel):
    id: int
    slug: str
    user: UserBase
    about: str


class CVDetail(CVBase):
    projects: List[CVProjectBase]


class CVDetailPublic(CVBase):
    user: UserProfile # override
    projects: List[CVProjectPublic]


class CVList(BaseModel):
    id: int
    slug: str
    about: str


class CreateCVBase(BaseModel):
    slug: Optional[str] = None
    about: str


class CreateCVBaseWithPosition(CreateCVBase):
    position: int
