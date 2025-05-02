from typing import Union, Annotated

from fastapi import status, HTTPException
from fastapi import Depends

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.user.models import User
from app.exceptions import ExistsError, NotExistsError, WrongCredentials
from app.database.core import get_db
