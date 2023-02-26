from fastapi import Depends, status, Response
from fastapi.responses import JSONResponse

from forum.db import users_table
from forum.db.models.abc import BaseUserManager
from forum.api.models import UserInfo, User


async def create_user(
    user: UserInfo, 
    users: BaseUserManager = Depends(users_table),
) -> Response:
    new_id = await users.insert(user)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            'user_id': new_id
        }
    )

async def get_all_users(
    users : BaseUserManager = Depends(users_table)
) -> list[User]:
    all_users = await users.select_all()
    return all_users


async def get_user(
    user_id: int, 
    users: BaseUserManager = Depends(users_table)
) -> Response:
    user = await users.select_by_id(user_id)
    if user is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": f"User with id {user_id} not found"}
        )
    return JSONResponse(
        content=user.dict()
    )

async def edit_user(
    user: User, 
    users: BaseUserManager = Depends(users_table)
) -> Response:
    ok = await users.update(user)
    if not ok:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": f"User with id {user.user_id} not found"}
        )
    return Response()
