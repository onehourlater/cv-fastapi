from sqlalchemy import select
from sqlalchemy.orm import Session

from .schema import CreateCVBaseWithPosition
from .models import CV
# from .schema import UpdateUserBase


def get_cvs_by_user(db: Session, user_id: int) -> CV:
    query = select(CV).where(CV.user_id == user_id)
    cvs = db.scalars(query).all()
    return cvs


def get_cv_by_id(db: Session, cv_id: int) -> CV:
    cv = db.get(CV, cv_id)
    return cv


def create_cv(db: Session, user_id: int, cv_data: CreateCVBaseWithPosition) -> CV:
    cv = CV(user_id=user_id, about=cv_data.about, position=cv_data.position)
    db.add(cv)
    db.commit()
    return cv


def is_cv_belongs_to_user(db: Session, cv_id: int, user_id: int) -> CV:
    cv = db.get(CV, cv_id)
    if cv.user_id == user_id:
        return True

    return False
