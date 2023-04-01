import uvicorn
from fastapi import FastAPI

from forum.core.events import create_start_app_handler, create_stop_app_handler
from forum.dependencies.settings import get_app_settings
from forum.routes import router


def get_application() -> FastAPI:
    app = FastAPI()
    app.include_router(router)

    settings = get_app_settings()
    app.add_event_handler(
        "startup",
        create_start_app_handler(app, settings),
    )
    app.add_event_handler(
        "shutdown",
        create_stop_app_handler(app),
    )
    return app


if __name__ == "__main__":
    app = get_application()
    uvicorn.run(app=app, port=8081, host="0.0.0.0")
