import json

from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from forum.api import router
from forum.repository import users_repo
from forum.api.models import User, UserId, UserInfo
from forum.repository.memory import (MemoryFriendshipRepository,
                                     MemoryUserRepository)

app = FastAPI()
app.include_router(router)


def test_post():
    app.dependency_overrides[users_repo] = MemoryUserRepository()
    client = TestClient(app)

    user_mock = UserInfo(name='lol', about='literally nothing', age=42, email='lol@tinkoff.ru')
    response = client.post('/users', content=user_mock.json())
    assert response.status_code == status.HTTP_201_CREATED


def test_empty():
    app.dependency_overrides[users_repo] = MemoryUserRepository()
    client = TestClient(app)

    response = client.get('/users')
    assert json.loads(response.content) == [] # здесь валится — в теле уже есть юзер с первого теста
