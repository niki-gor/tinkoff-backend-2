import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient

from alembic import command
from alembic.config import Config
from forum.core.app import get_application  # local import for testing purpose
from forum.models.domain import User
from forum.models.schemas import UserCredentials, UserInCreate

alembic_config = Config("alembic.test.ini")

user_mock = User(
    user_id=-1,
    name="lol",
    about="literally nothing",
    age=42,
    email="lol@example.com",
    last_login_at="2023",
)
user_mock_passwd = UserInCreate(**user_mock.dict(), password="123QQQqqq")


@pytest_asyncio.fixture(scope="function")
async def app() -> FastAPI:
    app = get_application()
    command.upgrade(alembic_config, "head")
    async with LifespanManager(app):
        yield app
    command.downgrade(alembic_config, "base")


@pytest_asyncio.fixture(scope="function")
async def client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client


async def get_authorization_headers(client, *, user_id: int) -> dict:
    response = await client.post(
        "/login",
        json=UserCredentials(**user_mock_passwd.dict(), user_id=user_id).dict(),
    )
    token = response.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    return headers
