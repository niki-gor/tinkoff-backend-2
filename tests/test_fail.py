from copy import deepcopy

from fastapi import status

from forum.api.errors import ErrAlreadyFriends, ErrUserNotFound
from forum.api.models import Error, User
from tests.common import client, new_app, user_mock


def test_method_not_allowed(new_app):
    response = client.patch("/users")
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_create_user_fail(new_app):
    response = client.post("/users")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    bad_params = [
        {"age": 1337},
        {"age": 0},
        {"name": ""},
        {"name": "a" * 100},
        {"about": "a" * 150},
        {"email": "notemail"},
    ]

    for bad_param in bad_params:
        bad_user = {**user_mock.dict(), **bad_param}
        response = client.post("/users", json=bad_user)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_user_fail(new_app):
    response = client.get("/users/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Error(**response.json()) == ErrUserNotFound

    response = client.get("/users/definitely_not_an_id")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_edit_user_fail(new_app):
    response = client.post("/users", json=user_mock.dict())

    response = client.put("/users/2", json=user_mock.dict())
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Error(**response.json()) == ErrUserNotFound

    bad_user = {**user_mock.dict(), "age": 1337}
    response = client.put("/users/1", json=bad_user)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_make_friendship_fail(new_app):
    response = client.put("/users/1/friends/2")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = client.post("/users", json=user_mock.dict())
    response = client.post("/users", json=user_mock.dict())
    response = client.put("/users/1/friends/2")

    response = client.put("/users/2/friends/1")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Error(**response.json()) == ErrAlreadyFriends

    response = client.put("/users/1/friends/2")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Error(**response.json()) == ErrAlreadyFriends
