from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator


class CVProjectBase(BaseModel):
    id: int
    title: str
    end_date: int
    role: str
    link: str
    description: str
    position: int

    @validator("end_date", pre=True)
    def convert_end_date_to_timestamp(cls, value):
        return value.timestamp()


class CVProjectPublic(BaseModel):
    id: int
    title: str
    end_date: int
    role: str
    link: str
    description: str
    position: int

    @validator("end_date", pre=True)
    def convert_end_date_to_timestamp(cls, value):
        return value.timestamp()



class CreateCVProject(BaseModel):
    title: str
    end_date: datetime
    role: Optional[str] = ''
    link: Optional[str] = ''
    description: Optional[str] = ''

    @validator("end_date", pre=True)
    def convert_timestamp_to_datetime(cls, value):
        if type(value) is not int:
            return value
        return datetime.fromtimestamp(value)

class CreateCVProjectWithPosition(CreateCVProject):
    position: int
