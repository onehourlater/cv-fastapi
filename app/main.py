import logging

from fastapi import FastAPI
from fastapi import Path

from app.database.core import Base, engine
from app.database.core import create_models, drop_create_models

from .routes import app_router


# SQLAlchemy
# drop_create_models()
create_models()


app_configs = {
    # 'openapi_url': None,
}
def get_application() -> FastAPI:
    application = FastAPI(**app_configs)
    application.include_router(
        app_router, prefix='/api/v1',
    )
    return application

app = get_application()
