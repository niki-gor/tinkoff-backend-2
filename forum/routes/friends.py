from fastapi import APIRouter, Depends, Response, status
from fastapi.exceptions import HTTPException

from forum.dependencies.authentication import authenticate_user_id
from forum.dependencies.database import get_friends_repo, get_users_repo
from forum.repositories.base import BaseFriendsRepository, BaseUsersRepository
from forum.resources import strings

router = APIRouter()


@router.put("/{to_id}", status_code=status.HTTP_201_CREATED, response_class=Response)
async def befriend(
    user_id: int,
    to_id: int,
    auth_user_id: int = Depends(authenticate_user_id),
    users: BaseUsersRepository = Depends(get_users_repo),
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
    for _id in [user_id, to_id]:
        user = await users.get_user_by_id(_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=strings.USER_NOT_FOUND
            )

    ok = await friendships.create_friends(user_id, to_id)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=strings.ALREADY_FRIENDS
        )
