from fastapi import FastAPI
from loguru import logger

from forum.routes import router
from forum.core.lifespan import lifespan


def get_application() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    app.router.lifespan_context = lifespan
    return app
