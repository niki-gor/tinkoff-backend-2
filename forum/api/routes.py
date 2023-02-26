from fastapi.routing import APIRoute

from forum.api.models import User
from forum.api.views.friendship import befriend
from forum.api.views.user import create_user, edit_user, get_all_users, get_user

ROUTES = [
    APIRoute("/user/new", create_user, methods=["POST"]),
    APIRoute("/user/all", get_all_users, response_model=list[User], methods=["GET"]),
    APIRoute("/user/id{user_id}", get_user, methods=["GET"]),
    APIRoute("/user/edit", edit_user, methods=["PUT"]),
    APIRoute("/friend/new", befriend, methods=["POST"]),
]
