import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from forum.models.domain import User

from forum.models.schemas import UserCredentials, UserInCreate
from forum.dependencies.database import friendships_repo, users_repo
from forum.repositories.memory import (MemoryFriendsRepository,
                                       MemoryUsersRepository)
from forum.routes import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)
user_mock = User(
    user_id=-1, name="lol", about="literally nothing", age=42, email="lol@tinkoff.ru", 
)
user_mock_passwd = UserInCreate(**user_mock.dict(), password="123QQQqqq")


@pytest.fixture
def new_app():
    app.dependency_overrides[users_repo] = MemoryUsersRepository()
    app.dependency_overrides[friendships_repo] = MemoryFriendsRepository()
    yield app
    app.dependency_overrides = {}


def get_authorization_headers(*, user_id: int) -> dict:
    response = client.post(
        "/login",
        json=UserCredentials(**user_mock_passwd.dict(), user_id=user_id).dict(),
    )
    token = response.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    return headers