from fastapi import APIRouter, Depends, Response, status
from fastapi.exceptions import HTTPException

from forum.models.domain import User, UserInfo
from forum.models.schemas import (ListOfUsersInResponse, UserIdInResponse,
                                  UserInfoInResponse, UserInfoWithPassword)
from forum.repositories import users_repo
from forum.repositories.abc import BaseUserRepository
from forum.resources import strings

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserIdInResponse)
async def create_user(
    user_info: UserInfoWithPassword,
    users: BaseUserRepository = Depends(users_repo),
) -> UserIdInResponse:
    new_id = await users.insert(user_info)
    return UserIdInResponse(user_id=new_id)


@router.get("", response_model=ListOfUsersInResponse)
async def get_all_users(users: BaseUserRepository = Depends(users_repo)) -> ListOfUsersInResponse:
    all_users = await users.select_all()
    return ListOfUsersInResponse(users=all_users)


@router.get("/{user_id}", response_model=UserInfoInResponse)
async def get_user(
    user_id: int, users: BaseUserRepository = Depends(users_repo)
) -> UserInfo:
    user_info = await users.select_by_id(user_id)
    if user_info is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=strings.USER_NOT_FOUND
        )
    return UserInfoInResponse(user_info=user_info)


@router.put(
    "/{user_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response
)
async def edit_user(
    user_id: int,
    user_info: UserInfo,
    users: BaseUserRepository = Depends(users_repo),
) -> None:
    ok = await users.update(user_id, user_info)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=strings.USER_NOT_FOUND
        )
