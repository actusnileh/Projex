from fastapi import FastAPI

from src.api.projects.handlers import router as tasks_router
from src.settings import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.SERVICE_NAME,
        debug=True,
    )

    app.include_router(
        tasks_router,
        prefix="/project",
    )

    return app
