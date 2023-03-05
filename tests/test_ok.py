from copy import deepcopy

from fastapi import status

from forum.models.domain import User
from tests.common import client, user_mock, new_app


def test_create_user(new_app):
    response = client.post("/users", json=user_mock.dict())
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"user_id": 1}


def test_get_all_users(new_app):
    response = client.get("/users")
    assert response.json()['users'] == []
    assert response.status_code == status.HTTP_200_OK

    response = client.post("/users", json=user_mock.dict())
    response = client.post("/users", json=user_mock.dict())

    response = client.get("/users")
    assert response.json()['users'] == [
        User(**user_mock.dict(), user_id=1),
        User(**user_mock.dict(), user_id=2),
    ]


def test_get_user(new_app):
    response = client.post("/users", json=user_mock.dict())

    response = client.get("/users/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['user_info'] == user_mock


def test_edit_user(new_app):
    response = client.post("/users", json=user_mock.dict())

    change = deepcopy(user_mock)
    change.about = user_mock.about + " difference"
    change.name = user_mock.name + " other name"
    response = client.put("/users/1", content=change.json())
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get("/users/1")
    assert response.json()['user_info'] == change


def test_make_friendship(new_app):
    response = client.post("/users", json=user_mock.dict())
    response = client.post("/users", json=user_mock.dict())

    response = client.put('/users/1/friends/2')
    assert response.status_code == status.HTTP_201_CREATED
