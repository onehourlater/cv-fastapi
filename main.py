import uvicorn

from app.main import get_application

app = get_application()

if __name__ == "__main__":
    uvicorn.run(app, loop="uvloop")
