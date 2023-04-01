import pytest
from fastapi import status

from forum.models.schemas import UserCredentials
from forum.resources import strings
from tests.conftest import get_authorization_headers, user_mock, user_mock_passwd

pytestmark = pytest.mark.asyncio


async def test_method_not_allowed(client):
    response = await client.patch("/users")
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


async def test_create_user_fail(client):
    response = await client.post("/users")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    bad_params = [
        {"age": 1337},
        {"age": 0},
        {"name": ""},
        {"name": "a" * 100},
        {"about": "a" * 150},
        {"email": "notemail"},
        {"password": "Qq1"},
        {"password": "aaabbb111"},
    ]

    for bad_param in bad_params:
        bad_user = {**user_mock_passwd.dict(), **bad_param}
        response = await client.post("/users", json=bad_user)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_get_user_fail(client):
    response = await client.get("/users/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == strings.USER_NOT_FOUND

    response = await client.get("/users/async definitely_not_an_id")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_edit_user_fail(client):
    response = await client.post("/users", json=user_mock_passwd.dict())
    headers = await get_authorization_headers(client, user_id=1)

    response = await client.put("/users/2", json=user_mock.dict(), headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == strings.INSUFFICIENT_PERMISSIONS
    # нельзя редактировать другого пользователя вне зависимости от того, создан он или нет
    response = await client.post("/users", json=user_mock_passwd.dict())
    response = await client.put("/users/2", json=user_mock.dict(), headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == strings.INSUFFICIENT_PERMISSIONS

    bad_user = {**user_mock.dict(), "age": 1337}
    response = await client.put("/users/1", json=bad_user, headers=headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_make_friendship_fail(client):
    response = await client.put("/users/1/friends/2")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = await client.post("/users", json=user_mock_passwd.dict())
    response = await client.post("/users", json=user_mock_passwd.dict())
    headers = await get_authorization_headers(client, user_id=1)

    response = await client.put("/users/1/friends/1", headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == strings.SAME_FRIENDS_IDS

    response = await client.put("/users/1/friends/2", headers=headers)

    response = await client.put("/users/1/friends/2", headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == strings.ALREADY_FRIENDS

    headers = await get_authorization_headers(client, user_id=2)
    response = await client.put("/users/2/friends/1", headers=headers)
    assert response.status_code == status.HTTP_201_CREATED

    response = await client.put("/users/2/friends/1", headers=headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == strings.ALREADY_FRIENDS


async def test_login_fail(client):
    response = await client.post(
        "/login",
        json=UserCredentials(user_id=1, password=user_mock_passwd.password).dict(),
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == strings.WRONG_ID_OR_PASSWD

    response = await client.post("/users", json=user_mock_passwd.dict())
    response = await client.post(
        "/login",
        json=UserCredentials(user_id=1, password="incorrect password").dict(),
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == strings.WRONG_ID_OR_PASSWD


async def test_chat_fail(client):
    response = await client.post("/users", json=user_mock_passwd.dict())
    response = await client.post("/users", json=user_mock_passwd.dict())
    headers = await get_authorization_headers(client, user_id=1)
    response = await client.put("/users/1/friends/2", headers=headers)

    response = await client.get("/users/1/chat/2")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = await client.get("/users/1/chat/2", headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == strings.CHAT_ONLY_FRIENDS
