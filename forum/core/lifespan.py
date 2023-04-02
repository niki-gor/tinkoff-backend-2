from contextlib import asynccontextmanager

from fastapi import FastAPI

from forum.db.connection import close_db_connection, connect_to_db
from forum.dependencies.settings import get_app_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_db(app, get_app_settings())
    yield
    await close_db_connection(app)
