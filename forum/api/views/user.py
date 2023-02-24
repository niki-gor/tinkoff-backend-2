from fastapi import Depends

from forum.db import users_table
from forum.db.models.abc import BaseUserManager
from forum.api.models import UserInfo, User, UserListResponse, UserResponse, OkResponse, UserIdResponse


async def create_user(user: UserInfo, users: BaseUserManager = Depends(users_table)) -> UserIdResponse:
    new_id = await users.insert(user)
    return UserIdResponse(user_id=new_id)


async def get_all_users(users : BaseUserManager = Depends(users_table)) -> UserListResponse:
    all_users = await users.select_all()
    return UserListResponse(users=all_users)


async def get_user(user_id: int, users: BaseUserManager = Depends(users_table)) -> UserResponse:
    user = await users.select_by_id(user_id)
    return UserResponse(user=user)


async def edit_user(user: User, users: BaseUserManager = Depends(users_table)) -> OkResponse:
    ok = await users.update(user)
    return OkResponse(ok=ok)
