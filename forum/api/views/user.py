from fastapi import Depends, status, Response

from forum.repository import users_table
from forum.repository.abc import BaseUserRepository
from forum.api.models import UserInfo, User, Error, EmptyBody, UserId


async def create_user(
    user_info: UserInfo, 
    r: Response,
    users: BaseUserRepository = Depends(users_table),
) -> UserId:
    new_id = await users.insert(user_info)
    r.status_code = status.HTTP_201_CREATED
    return UserId(user_id=new_id)


async def get_all_users(
    users : BaseUserRepository = Depends(users_table)
) -> list[User]:
    all_users = await users.select_all()
    return all_users


async def get_user(
    user_id: int, 
    r: Response,
    users: BaseUserRepository = Depends(users_table)
) -> UserInfo | Error:
    user_info = await users.select_by_id(user_id)
    if user_info is None:
        r.status_code = status.HTTP_404_NOT_FOUND
        return Error(detail=f"User with id {user_id} not found")
    return user_info


async def edit_user(
    user_id: int,
    user_info: UserInfo,
    r: Response,
    users: BaseUserRepository = Depends(users_table)
) -> Error | EmptyBody:
    ok = await users.update(user_id, user_info)
    if not ok:
        r.status_code = status.HTTP_400_BAD_REQUEST
        return Error(detail=f"User with id {user_id} not found")
    return {}
