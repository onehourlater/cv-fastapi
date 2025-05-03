from sqlalchemy import select
from sqlalchemy.orm import Session

from .schema import CreateCVProjectWithPosition
from ..models import CVProject


def get_cv_projects(db: Session, cv_id: int) -> CVProject:
    query = select(CVProject).where(CVProject.cv_id == cv_id)
    cv_projects = db.scalars(query).all()
    return cv_projects


def create_cv_project(
    db: Session, cv_id: int, project_data: CreateCVProjectWithPosition
) -> CVProject:
    cv_project = CVProject(
        cv_id=cv_id,
        title=project_data.title,
        end_date=project_data.end_date,
        role=project_data.role,
        link=project_data.link,
        description=project_data.description,
        position=project_data.position,
    )
    db.add(cv_project)
    db.commit()
    return cv_project
