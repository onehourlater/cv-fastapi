from typing import List

from fastapi import Depends

from app.exceptions import NoPermission
from app.database.core import get_db, Session

from app.user.models import User

from .models import PublicStatus
from .schema import CVBase, CVDetail, CreateCVBase, CreateCVBaseWithPosition
from .service import get_cvs_by_user, get_cv_by_id, create_cv, is_cv_belongs_to_user
from .project.schema import CreateCVProjectWithPosition
from .project.service import get_cv_projects, create_cv_project


class CVManager:
    def __init__(self, db: Session):
        self.db = db

    def get_cvs_by_user(self, user: User) -> List[CVBase]:
        return get_cvs_by_user(self.db, user.id)

    def get_cv_by_id(self, user: User, cv_id) -> CVDetail:
        if not is_cv_belongs_to_user(self.db, cv_id, user.id):
            raise NoPermission('CV does not belong to User')

        return get_cv_by_id(self.db, cv_id)

    def get_public_cv_by_id(self, user: User, cv_id) -> CVDetail:
        cv = get_cv_by_id(self.db, cv_id)

        if user and user.id == cv.user_id:
            return cv

        if cv.public_status == PublicStatus.PRIVATE:
            raise NoPermission('CV is private')

        return cv

    def create_cv(self, user: User, cv_data: CreateCVBase) -> CVBase:
        user_cvs = get_cvs_by_user(self.db, user.id)
        cv_data_to_create = CreateCVBaseWithPosition(
            about=cv_data.about, position=len(user_cvs) + 1
        )

        return create_cv(self.db, user.id, cv_data_to_create)

    def get_cv_project(self, user: User, cv_id: int):
        if not is_cv_belongs_to_user(self.db, cv_id, user.id):
            raise NoPermission('CV does not belong to User')

        return get_cv_projects(self.db, cv_id)

    def create_cv_project(self, user: User, cv_id: int, cv_project_data: CreateCVBase):
        if not is_cv_belongs_to_user(self.db, cv_id, user.id):
            raise NoPermission('CV does not belong to User')

        cv_projects = get_cv_projects(self.db, cv_id)
        project_data_to_create = CreateCVProjectWithPosition(
            title=cv_project_data.title,
            end_date=cv_project_data.end_date,
            role=cv_project_data.role,
            link=cv_project_data.link,
            description=cv_project_data.description,
            position=len(cv_projects) + 1,
        )

        return create_cv_project(self.db, cv_id, project_data_to_create)


def get_cv_manager(db: Session = Depends(get_db)) -> CVManager:
    return CVManager(db)


#
