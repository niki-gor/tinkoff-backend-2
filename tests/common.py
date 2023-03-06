import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from forum.models.domain import UserInfo
from forum.models.schemas import UserInfoWithPassword
from forum.repositories import friendships_repo, users_repo
from forum.repositories.memory import (MemoryFriendshipRepository,
                                       MemoryUserRepository)
from forum.routes import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)
user_mock = UserInfo(
    name="lol", about="literally nothing", age=42, email="lol@tinkoff.ru"
)
user_mock_passwd = UserInfoWithPassword(**user_mock.dict(), password='qwerty123')


@pytest.fixture
def new_app():
    app.dependency_overrides[users_repo] = MemoryUserRepository()
    app.dependency_overrides[friendships_repo] = MemoryFriendshipRepository()
    yield app
    app.dependency_overrides = {}
