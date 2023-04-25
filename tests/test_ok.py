from copy import deepcopy

import pytest
from fastapi import status
from loguru import logger

from forum.models.schemas import UserCredentials
from tests.conftest import get_authorization_headers, user_mock, user_mock_passwd

pytestmark = pytest.mark.asyncio


async def test_create_user(client):
    response = await client.post("/users", json=user_mock_passwd.dict())
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"user_id": 1}


async def test_get_all_users(client):
    response = await client.get("/users")
    assert response.json()["users"] == []
    assert response.status_code == status.HTTP_200_OK

    response = await client.post("/users", json=user_mock_passwd.dict())
    response = await client.post("/users", json=user_mock_passwd.dict())

    response = await client.get("/users")
    assert sorted(response.json()["users"], key=lambda item: item["user_id"]) == [
        user_mock.copy(update={"user_id": 1}),
        user_mock.copy(update={"user_id": 2}),
    ]


async def test_get_user(client):
    response = await client.post("/users", json=user_mock_passwd.dict())

    response = await client.get("/users/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["user"] == user_mock.copy(update={"user_id": 1})


async def test_edit_user(client):
    response = await client.post("/users", json=user_mock_passwd.dict())
    headers = await get_authorization_headers(client, user_id=1)

    change = deepcopy(user_mock)
    change.about = user_mock.about + " difference"
    change.name = user_mock.name + " other name"
    response = await client.put("/users/1", content=change.json(), headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = await client.get("/users/1")
    assert response.json()["user"] == change.copy(update={"user_id": 1})


async def test_make_friendship(client):
    response = await client.post("/users", json=user_mock_passwd.dict())
    response = await client.post("/users", json=user_mock_passwd.dict())
    headers = await get_authorization_headers(client, user_id=1)

    response = await client.put("/users/1/friends/2", headers=headers)
    assert response.status_code == status.HTTP_201_CREATED


async def test_login(client):
    response = await client.post("/users", json=user_mock_passwd.dict())
    response = await client.post(
        "/login",
        json=UserCredentials(user_id=1, password=user_mock_passwd.password).dict(),
    )
    assert response.status_code == status.HTTP_201_CREATED


async def test_chat(client):
    response = await client.post("/users", json=user_mock_passwd.dict())
    response = await client.post("/users", json=user_mock_passwd.dict())
    headers = await get_authorization_headers(client, user_id=1)
    response = await client.put("/users/1/friends/2", headers=headers)
    headers = await get_authorization_headers(client, user_id=2)
    response = await client.put("/users/2/friends/1", headers=headers)

    response = await client.get("/users/2/chat/1", headers=headers)
    assert response.status_code == status.HTTP_200_OK


async def test_get_friends(client):
    response = await client.post("/users", json=user_mock_passwd.dict())
    response = await client.post("/users", json=user_mock_passwd.dict())
    headers = await get_authorization_headers(client, user_id=1)

    response = await client.put("/users/1/friends/2", headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    response = await client.get("users/1/friends")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["users"] == []

    headers = await get_authorization_headers(client, user_id=2)
    response = await client.put("/users/2/friends/1", headers=headers)

    response = await client.get("users/1/friends")
    result = response.json()["users"]
    result[0].pop("last_login_at")
    required = [user_mock.copy(update={"user_id": 2}).dict()]
    required[0].pop("last_login_at")
    assert result == required
