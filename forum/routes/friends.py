from fastapi import APIRouter, Depends, Response, status
from fastapi.exceptions import HTTPException

from forum.dependencies.authentication import authenticate_user_id
from forum.dependencies.database import get_friends_repo
from forum.models.schemas import ListOfUsersInResponse
from forum.repositories.base import BaseFriendsRepository
from forum.resources import strings

router = APIRouter()


@router.put("/{to_id}", status_code=status.HTTP_201_CREATED, response_class=Response)
async def befriend(
    user_id: int,
    to_id: int,
    auth_user_id: int = Depends(authenticate_user_id),
    friendships: BaseFriendsRepository = Depends(get_friends_repo),
) -> None:
    if user_id != auth_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.INSUFFICIENT_PERMISSIONS,
        )
    if user_id == to_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=strings.SAME_FRIENDS_IDS
        )
    try:
        await friendships.create_friends(user_id, to_id)
    except ValueError as e:
        codes = {
            strings.USER_NOT_FOUND: status.HTTP_404_NOT_FOUND,
            strings.ALREADY_FRIENDS: status.HTTP_400_BAD_REQUEST,
        }
        raise HTTPException(status_code=codes[str(e)], detail=str(e))


@router.get("", response_model=ListOfUsersInResponse)
async def get_friends(
    user_id: int, friendships: BaseFriendsRepository = Depends(get_friends_repo)
) -> ListOfUsersInResponse:
    friends = await friendships.get_friends(user_id)
    return ListOfUsersInResponse(users=friends)
