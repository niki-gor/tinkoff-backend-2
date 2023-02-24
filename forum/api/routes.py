from fastapi.routing import APIRoute

from forum.api.models import (UserIdResponse, OkResponse, UserListResponse,
                              UserResponse)
from forum.api.views.friendship import befriend
from forum.api.views.user import (create_user, edit_user, get_all_users,
                                  get_user)

ROUTES = [
    APIRoute("/user", create_user, response_model=UserIdResponse, methods=["POST"]),
    APIRoute(
        "/user/list", get_all_users, response_model=UserListResponse, methods=["GET"]
    ),
    APIRoute(
        "/user/id{user_id}", get_user, response_model=UserResponse, methods=["GET"]
    ),
    APIRoute("/user", edit_user, response_model=OkResponse, methods=["PUT"]),

    APIRoute("/friend", befriend, response_model=OkResponse, methods=["PUT"]),
]
