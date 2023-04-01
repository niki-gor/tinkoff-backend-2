import uvicorn

from forum.core.app import get_application

if __name__ == "__main__":
    app = get_application()
    uvicorn.run(app=app, port=8081, host="0.0.0.0")
