from fastapi import APIRouter, Depends, Response, status
from fastapi.exceptions import HTTPException
from forum.core.config import AppSettings
from forum.dependencies.authentication import auth_user_id
from forum.models.domain import User

from forum.models.schemas import (
    ListOfUsersInResponse,
    UserCredentials,
    UserIdInResponse,
    UserInResponse,
    UserInUpdate,
    JWTUser,
    UserInCreate,
    UserWithToken,
)
from forum.dependencies.database import users_repo
from forum.repositories.base import BaseUsersRepository
from forum.resources import strings
from forum.services import jwt
from forum.core.config import app_settings, AppSettings

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserIdInResponse)
async def create_user(
    user_info: UserInCreate,
    users: BaseUsersRepository = Depends(users_repo),
) -> UserIdInResponse:
    new_id = await users.insert(**user_info.dict())
    return UserIdInResponse(user_id=new_id)


@router.get("", response_model=ListOfUsersInResponse)
async def get_all_users(
    users: BaseUsersRepository = Depends(users_repo),
) -> ListOfUsersInResponse:
    all_users = await users.select_all()
    return ListOfUsersInResponse(users=all_users)


@router.get("/{user_id}", response_model=UserInResponse)
async def get_user(
    user_id: int, users: BaseUsersRepository = Depends(users_repo)
) -> UserInResponse:
    user_with_passwd = await users.select_by_id(user_id)
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
    user_id: int,
    user_info: UserInUpdate,
    auth_user_id: int = Depends(auth_user_id),
    users: BaseUsersRepository = Depends(users_repo),
) -> None:
    if user_id != auth_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=strings.INSUFFICIENT_PERMISSIONS_TO_EDIT)

    ok = await users.update(user_id=user_id, **user_info.dict())
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=strings.USER_NOT_FOUND
        )
