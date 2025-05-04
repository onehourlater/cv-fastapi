from sqlalchemy import select, func
from sqlalchemy.orm import Session

from .schema import CreateCVBaseWithPosition
from .models import CV
from .utils import generate_random_string
# from .schema import UpdateUserBase


def get_cvs_by_user(db: Session, user_id: int) -> CV:
    query = select(CV).where(CV.user_id == user_id)
    cvs = db.scalars(query).all()
    return cvs


def get_cv_by_id(db: Session, cv_id: int) -> CV:
    cv = db.get(CV, cv_id)
    return cv


def get_cv_by_slug(db: Session, cv_slug: str) -> CV:
    query = select(CV).where(CV.slug == cv_slug)
    cv = db.scalars(query).one_or_none()
    return cv


def check_if_cv_slug_is_unique(db: Session, cv_slug: str) -> bool:
    query = select(func.count(CV.id)).filter(CV.slug==cv_slug).select_from(CV)
    cv_count = db.scalar(query)
    return True if cv_count == 0 else False


def generate_unique_cv_slug(db: Session) -> bool:
    MAX_LIMIT = 10
    new_slug = generate_random_string(6)
    limit = 0
    while True and limit < MAX_LIMIT:
        limit += 1
        if check_if_cv_slug_is_unique(db, new_slug):
            break

    if limit >= MAX_LIMIT:
        raise ValueError('Cant find unique slug for cv, try again later')

    return new_slug


def create_cv(db: Session, user_id: int, cv_data: CreateCVBaseWithPosition) -> CV:
    cv = CV(user_id=user_id, slug=cv_data.slug, about=cv_data.about, position=cv_data.position)
    db.add(cv)
    db.commit()
    return cv


def is_cv_belongs_to_user(db: Session, cv_id: int, user_id: int) -> CV:
    cv = db.get(CV, cv_id)
    if cv.user_id == user_id:
        return True

    return False
