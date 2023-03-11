from fastapi import APIRouter, Depends, Response, status
from fastapi.exceptions import HTTPException

from forum.repositories import friendships_repo, users_repo
from forum.repositories.abc import BaseFriendsRepository, BaseUsersRepository
from forum.resources import strings

router = APIRouter()


@router.put("/{to_id}", status_code=status.HTTP_201_CREATED, response_class=Response)
async def befriend(
    user_id: int,
    to_id: int,
    users: BaseUsersRepository = Depends(users_repo),
    friendships: BaseFriendsRepository = Depends(friendships_repo),
) -> None:
    if user_id == to_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=strings.SAME_FRIENDS_IDS
        )
    for _id in [user_id, to_id]:
        user = await users.select_by_id(_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=strings.USER_NOT_FOUND
            )

    ok = await friendships.insert(user_id, to_id)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=strings.ALREADY_FRIENDS
        )
