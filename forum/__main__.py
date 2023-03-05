import uvicorn
from fastapi import FastAPI
from forum.routes import router


app = FastAPI()
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app=app, port=8000, host="127.0.0.1")
