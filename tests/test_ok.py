from copy import deepcopy

from fastapi import status
from forum.models.domain import User
from forum.models.schemas import UserCredentials

from tests.common import (
    client,
    get_authorization_headers,
    new_app,
    user_mock,
    user_mock_passwd,
)


def test_create_user(new_app):
    response = client.post("/users", json=user_mock_passwd.dict())
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"user_id": 1}


def test_get_all_users(new_app):
    response = client.get("/users")
    assert response.json()["users"] == []
    assert response.status_code == status.HTTP_200_OK

    response = client.post("/users", json=user_mock_passwd.dict())
    response = client.post("/users", json=user_mock_passwd.dict())

    response = client.get("/users")
    assert response.json()["users"] == [
        user_mock.copy(update={"user_id": 1}),
        user_mock.copy(update={"user_id": 2}),
    ]


def test_get_user(new_app):
    response = client.post("/users", json=user_mock_passwd.dict())

    response = client.get("/users/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["user"] == user_mock.copy(update={"user_id": 1})


def test_edit_user(new_app):
    response = client.post("/users", json=user_mock_passwd.dict())
    headers = get_authorization_headers(user_id=1)

    change = deepcopy(user_mock)
    change.about = user_mock.about + " difference"
    change.name = user_mock.name + " other name"
    response = client.put("/users/1", content=change.json(), headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get("/users/1")
    assert response.json()["user"] == change.copy(update={"user_id": 1})


def test_make_friendship(new_app):
    response = client.post("/users", json=user_mock_passwd.dict())
    response = client.post("/users", json=user_mock_passwd.dict())
    headers = get_authorization_headers(user_id=1)

    response = client.put("/users/1/friends/2", headers=headers)
    assert response.status_code == status.HTTP_201_CREATED


def test_login(new_app):
    response = client.post("/users", json=user_mock_passwd.dict())
    response = client.post(
        "/login",
        json=UserCredentials(user_id=1, password=user_mock_passwd.password).dict(),
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_chat(new_app):
    response = client.post("/users", json=user_mock_passwd.dict())
    response = client.post("/users", json=user_mock_passwd.dict())
    headers = get_authorization_headers(user_id=1)
    response = client.put("/users/1/friends/2", headers=headers)
    headers = get_authorization_headers(user_id=2)
    response = client.put("/users/2/friends/1", headers=headers)

    response = client.get("/users/2/chat/1", headers=headers)
    assert response.status_code == status.HTTP_200_OK
