import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import AppSettings
from app.database.core import drop_models, create_models

from .routes import app_router


# creates media folder if doesnt exists
media_folder_path = AppSettings.MEDIA_FOLDER_PATH
if not media_folder_path:
    raise Exception('MEDIA_FOLDER_PATH is not specified')

if not os.path.exists(media_folder_path):
    os.mkdir(media_folder_path)

# Drop models if needed
if False:
    drop_models()

create_models()

app_configs = {
    # 'openapi_url': None,
}

def get_application() -> FastAPI:
    application = FastAPI(**app_configs)
    application.include_router(
        app_router,
        prefix='/api/v1',
    )
    application.mount('/media', StaticFiles(directory=AppSettings.MEDIA_FOLDER_PATH), name='media')

    return application


app = get_application()
