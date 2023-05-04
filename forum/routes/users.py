from fastapi import APIRouter, Depends, Response, status
from fastapi.exceptions import HTTPException

from forum.dependencies.authentication import authenticate_user_id
from forum.dependencies.database import get_users_repo
from forum.models.domain import User
from forum.models.schemas import (
    UserIdInResponse,
    UserInCreate,
    UserInResponse,
    UserInUpdate,
)
from forum.repositories.base import BaseUsersRepository
from forum.resources import strings

router = APIRouter()


async def validate_user_id(user_id: int) -> int:
    if not (-2147483648 <= user_id and user_id <= 2147483647):  # int32
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=strings.USER_NOT_FOUND
        )
    return user_id


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserIdInResponse)
async def create_user(
    user_info: UserInCreate,
    users: BaseUsersRepository = Depends(get_users_repo),
) -> UserIdInResponse:
    new_id = await users.create_user(**user_info.dict())
    return UserIdInResponse(user_id=new_id)


@router.get("/{user_id}", response_model=UserInResponse)
async def get_user(
    user_id: int = Depends(validate_user_id),
    users: BaseUsersRepository = Depends(get_users_repo),
) -> UserInResponse:
    user_with_passwd = await users.get_user_by_id(user_id)
    if user_with_passwd is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=strings.USER_NOT_FOUND
        )
    user = User(**user_with_passwd.dict())
    return UserInResponse(user=user)


@router.put(
    "/{user_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response
)
async def edit_user(
    user_info: UserInUpdate,
    user_id: int = Depends(validate_user_id),
    auth_user_id: int = Depends(authenticate_user_id),
    users: BaseUsersRepository = Depends(get_users_repo),
) -> None:
    if user_id != auth_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.INSUFFICIENT_PERMISSIONS,
        )

    updated = await users.update_user_by_id(user_id=user_id, **user_info.dict())
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=strings.USER_NOT_FOUND
        )
