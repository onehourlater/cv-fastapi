from typing import Union, List

from pydantic import BaseModel


class UserBase(BaseModel):
    id: int
    email: str
    username: str

class CreateUserBase(BaseModel):
    email: str
    password: str

class UserProfile(UserBase):
    full_name: Union[str, None] = None
    kind_of_activity: Union[str, None] = None
    about: Union[str, None] = None

class UpdateUserBase(BaseModel):
    full_name: str
    kind_of_activity: Union[str, None]
    about: Union[str, None]

class UsersDevInfo(BaseModel):
    users: List[UserBase]
    users_count: int
