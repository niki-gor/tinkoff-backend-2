import uvicorn
from fastapi import FastAPI

from forum.api.routes import ROUTES

app = FastAPI(routes=ROUTES)

if __name__ == "__main__":
    uvicorn.run(app=app, port=8000, host="127.0.0.1")
    