from fastapi import APIRouter

from app.auth.views import auth_router
from app.user.views import user_router
from app.cv.views import cv_router

'''
router = APIRouter()
router.include_router(item.router, tags=["item"], prefix="/item")
'''

app_router = APIRouter()

app_router.include_router(auth_router)
app_router.include_router(user_router)
app_router.include_router(cv_router)
