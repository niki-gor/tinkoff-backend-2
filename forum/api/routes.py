from fastapi.routing import APIRoute

from forum.api.models import User, UserInfo, Error, EmptyBody, UserId
from forum.api.views.friendship import befriend
from forum.api.views.user import create_user, edit_user, get_all_users, get_user

ROUTES = [
    APIRoute("/users", create_user, response_model = UserId, methods=["POST"]),
    APIRoute("/users", get_all_users, response_model = list[User], methods=["GET"]),
    APIRoute("/users/{user_id}", get_user, response_model = UserInfo | Error, methods=["GET"]),
    APIRoute("/users/{user_id}", edit_user, response_model = Error | EmptyBody, methods=["PUT"]),
    APIRoute("/friends", befriend, response_model = Error | EmptyBody, methods=["PUT"]),
]
