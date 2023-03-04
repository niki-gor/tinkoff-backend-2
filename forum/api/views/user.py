from fastapi import Depends, Response, status

from forum.api.errors import ErrUserNotFound
from forum.api.models import EmptyBody, Error, User, UserId, UserInfo
from forum.repository import users_repo
from forum.repository.abc import BaseUserRepository


async def create_user(
    user_info: UserInfo,
    r: Response,
    users: BaseUserRepository = Depends(users_repo),
) -> UserId:
    new_id = await users.insert(user_info)
    r.status_code = status.HTTP_201_CREATED
    return UserId(user_id=new_id)


async def get_all_users(users: BaseUserRepository = Depends(users_repo)) -> list[User]:
    all_users = await users.select_all()
    return all_users


async def get_user(
    user_id: int, r: Response, users: BaseUserRepository = Depends(users_repo)
) -> UserInfo | Error:
    user_info = await users.select_by_id(user_id)
    if user_info is None:
        r.status_code = status.HTTP_404_NOT_FOUND
        return ErrUserNotFound
    return user_info


async def edit_user(
    user_id: int,
    user_info: UserInfo,
    r: Response,
    users: BaseUserRepository = Depends(users_repo),
) -> Error | EmptyBody:
    ok = await users.update(user_id, user_info)
    if not ok:
        r.status_code = status.HTTP_404_NOT_FOUND
        return ErrUserNotFound
    return {}
