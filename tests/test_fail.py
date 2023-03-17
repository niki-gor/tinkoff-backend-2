from fastapi import status
from forum.models.schemas import UserCredentials

from forum.resources import strings
from tests.common import client, new_app, user_mock, user_mock_passwd


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
        {"password": "Qq1"},
        {"password": "aaabbb111"},
    ]

    for bad_param in bad_params:
        bad_user = {**user_mock_passwd.dict(), **bad_param}
        response = client.post("/users", json=bad_user)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_user_fail(new_app):
    response = client.get("/users/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == strings.USER_NOT_FOUND

    response = client.get("/users/definitely_not_an_id")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_edit_user_fail(new_app):
    response = client.post("/users", json=user_mock_passwd.dict())
    response = client.post(
        "/login",
        json=UserCredentials(**user_mock_passwd.dict(), **response.json()).dict(),
    )
    token = response.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.put("/users/2", json=user_mock.dict(), headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == strings.INSUFFICIENT_PERMISSIONS_TO_EDIT
    # нельзя редактировать другого пользователя вне зависимости от того, создан он или нет
    response = client.post("/users", json=user_mock_passwd.dict())
    response = client.put("/users/2", json=user_mock.dict(), headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['detail'] == strings.INSUFFICIENT_PERMISSIONS_TO_EDIT

    bad_user = {**user_mock.dict(), "age": 1337}
    response = client.put("/users/1", json=bad_user, headers=headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_make_friendship_fail(new_app):
    response = client.put("/users/1/friends/2")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    response = client.post("/users", json=user_mock_passwd.dict())
    response = client.post("/users", json=user_mock_passwd.dict())

    response = client.put("/users/1/friends/1")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == strings.SAME_FRIENDS_IDS

    response = client.put("/users/1/friends/2")

    response = client.put("/users/1/friends/2")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == strings.ALREADY_FRIENDS

    response = client.put("/users/2/friends/1")
    assert response.status_code == status.HTTP_201_CREATED

    response = client.put("/users/2/friends/1")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == strings.ALREADY_FRIENDS
