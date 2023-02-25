from fastapi.routing import APIRoute
from fastapi import Response
from fastapi.responses import JSONResponse

from forum.api.models import (UserIdResponse, OkResponse, UserListResponse,
                              UserResponse, User)
from forum.api.views.friendship import befriend
from forum.api.views.user import (create_user, edit_user, get_all_users,
                                  get_user)

ROUTES = [
    APIRoute("/user", create_user, response_model=UserIdResponse, methods=["POST"]),
    APIRoute(
        "/user/list", get_all_users, response_model=list[User], methods=["GET"]
    ),
    APIRoute(
        "/user/id{user_id}", get_user, methods=["GET"]
    ),
    APIRoute("/user", edit_user, response_model=OkResponse, methods=["PUT"]),

    APIRoute("/friend", befriend, response_model=OkResponse, methods=["PUT"]),
]
