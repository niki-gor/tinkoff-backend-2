from fastapi import APIRouter, Depends, Response, status
from fastapi.exceptions import HTTPException

from forum.models.domain import User, UserInfo
from forum.models.schemas import UserId
from forum.repository import users_repo
from forum.repository.abc import BaseUserRepository
from forum.resources import strings

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserId)
async def create_user(
    user_info: UserInfo,
    users: BaseUserRepository = Depends(users_repo),
) -> UserId:
    new_id = await users.insert(user_info)
    return UserId(user_id=new_id)


@router.get("", response_model=list[User])
async def get_all_users(users: BaseUserRepository = Depends(users_repo)) -> list[User]:
    all_users = await users.select_all()
    return all_users


@router.get("/{user_id}", response_model=UserInfo)
async def get_user(
    user_id: int, users: BaseUserRepository = Depends(users_repo)
) -> UserInfo:
    user_info = await users.select_by_id(user_id)
    if user_info is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=strings.USER_NOT_FOUND
        )
    return user_info


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
