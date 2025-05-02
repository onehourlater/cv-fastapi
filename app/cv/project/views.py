import logging

from typing import List

from fastapi import APIRouter, HTTPException
from fastapi import Depends

from app.exceptions import NoPermission

from app.auth.manager import get_current_user
from app.user.models import User

from ..manager import CVManager, get_cv_manager
from .schema import CreateCVProject, CVProjectPublic

log = logging.getLogger(__name__)

# /api/v1/cv/{cv_id}/project
cv_project_router = APIRouter(prefix='/{cv_id}/projects')


@cv_project_router.get('/')
async def get_cv_projects_list(
    *,
    current_user: User = Depends(get_current_user),
    cv_manager: CVManager = Depends(get_cv_manager),
    cv_id: int,
) -> List[CVProjectPublic]:
    try:
        cv_list = cv_manager.get_cv_project(current_user, cv_id)
    except NoPermission as e:
        raise HTTPException(403, str(e))
    except Exception as e:
        log.error(
            f'error occured on cv_project_router /get_cv_projects_list handler {e}'
        )
        raise HTTPException(500, 'Error occured')

    return cv_list


@cv_project_router.post('/')
async def create_cv_project(
    *,
    current_user: User = Depends(get_current_user),
    cv_manager: CVManager = Depends(get_cv_manager),
    cv_id: int,
    cv_project_data: CreateCVProject,
) -> CVProjectPublic:
    print()
    print('cv_project_data cv_project_data: ', cv_project_data)
    cv = cv_manager.create_cv_project(current_user, cv_id, cv_project_data)
    return cv


#
