from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CVProjectBase(BaseModel):
    id: int
    title: str
    end_date: datetime
    client: str
    link: str
    description: str


class CVProjectPublic(BaseModel):
    id: int
    title: str
    end_date: datetime
    client: str
    link: str
    description: str
    position: int


class CreateCVProject(BaseModel):
    title: str
    end_date: datetime
    client: Optional[str] = ''
    link: Optional[str] = ''
    description: Optional[str] = ''


class CreateCVProjectWithPosition(CreateCVProject):
    position: int
