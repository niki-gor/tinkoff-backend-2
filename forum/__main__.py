import uvicorn

from forum.core.app import get_application
from prometheus_fastapi_instrumentator import Instrumentator


if __name__ == "__main__":
    app = get_application()
    Instrumentator().instrument(app).expose(app)

    uvicorn.run(app=app, port=8081, host="0.0.0.0")
