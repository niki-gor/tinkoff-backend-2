from copy import deepcopy

import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from forum.api import router
from forum.api.models import User, UserInfo
from forum.repository import friendships_repo, users_repo
from forum.repository.memory import (MemoryFriendshipRepository,
                                     MemoryUserRepository)

app = FastAPI()
app.include_router(router)
client = TestClient(app)
user_mock = UserInfo(
    name="lol", about="literally nothing", age=42, email="lol@tinkoff.ru"
)


@pytest.fixture
def new_app():
    app.dependency_overrides[users_repo] = MemoryUserRepository()
    app.dependency_overrides[friendships_repo] = MemoryFriendshipRepository()
    yield app
    app.dependency_overrides = {}


def test_create_user(new_app):
    response = client.post("/users", content=user_mock.json())
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"user_id": 1}


def test_get_all_users(new_app):
    response = client.get("/users")
    assert response.json() == []
    assert response.status_code == status.HTTP_200_OK

    response = client.post("/users", content=user_mock.json())
    response = client.post("/users", content=user_mock.json())

    response = client.get("/users")
    assert response.json() == [
        User(**user_mock.dict(), user_id=1),
        User(**user_mock.dict(), user_id=2),
    ]


def test_get_user(new_app):
    response = client.post("/users", content=user_mock.json())

    response = client.get("/users/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == user_mock


def test_edit_user(new_app):
    response = client.post("/users", content=user_mock.json())

    change = deepcopy(user_mock)
    change.about = user_mock.about + " difference"
    change.name = user_mock.name + " other name"
    response = client.put("/users/1", content=change.json())
    assert response.status_code == status.HTTP_200_OK

    response = client.get("/users/1")
    assert response.json() == change


def test_make_friendship(new_app):
    response = client.post("/users", content=user_mock.json())
    response = client.post("/users", content=user_mock.json())

    response = client.put('/users/1/friends/2')
    assert response.status_code == status.HTTP_201_CREATED
