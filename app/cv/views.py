import logging

from typing import Annotated, List

from fastapi import APIRouter, HTTPException
from fastapi import Depends, Path

from app.config import AppSettings
from app.exceptions import NoPermission, NotExistsError
from app.auth.manager import get_current_user
from app.user.models import User

from .project.views import cv_project_router

from .manager import CVManager, get_cv_manager
from .schema import CVList, CVDetail, CVDetailPublic, CreateCVBase


log = logging.getLogger(__name__)

cv_router = APIRouter(prefix='/cvs')
cv_router.include_router(cv_project_router)


@cv_router.get('/')
async def get_cv_list(
    current_user: User = Depends(get_current_user(required=True)),
    cv_manager: CVManager = Depends(get_cv_manager),
) -> List[CVList]:
    cv_list = cv_manager.get_cvs_by_user(current_user)
    return cv_list


@cv_router.get('/{cv_id}')
async def get_cv(
    *,
    current_user: User = Depends(get_current_user(required=True)),
    cv_manager: CVManager = Depends(get_cv_manager),
    cv_id: int,
) -> CVDetail:
    try:
        cv = cv_manager.get_cv_by_id(current_user, cv_id)
    except NoPermission as e:
        raise HTTPException(403, str(e))
    return cv

@cv_router.get('/{cv_slug}/public')
async def get_cv_public(
    *,
    current_user: User = Depends(get_current_user(required=False)),
    cv_manager: CVManager = Depends(get_cv_manager),
    cv_slug: Annotated[str, Path(pattern=AppSettings.CV_SLUG_PATTERN)],
) -> CVDetailPublic:
    try:
        cv = cv_manager.get_public_cv_by_slug(current_user, cv_slug)
    except NotExistsError as e:
        raise HTTPException(404, str(e))
    except NoPermission as e:
        raise HTTPException(403, str(e))
    return cv

@cv_router.post('/')
async def create_cv(
    *,
    current_user: User = Depends(get_current_user(required=True)),
    cv_manager: CVManager = Depends(get_cv_manager),
    cv_data: CreateCVBase,
) -> CVDetail:
    try:
        cv = cv_manager.create_cv(current_user, cv_data)
    except ValueError as e:
        raise HTTPException(403, str(e))

    return cv


#
