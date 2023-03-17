from copy import deepcopy

from fastapi import status
from forum.models.domain import User
from forum.models.schemas import UserCredentials

from tests.common import client, new_app, user_mock, user_mock_passwd


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
    response = client.post(
        "/login",
        json=UserCredentials(**user_mock_passwd.dict(), **response.json()).dict(),
    )
    token = response.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

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

    response = client.put("/users/1/friends/2")
    assert response.status_code == status.HTTP_201_CREATED
