from fastapi import APIRouter, Depends, Response, status
from fastapi.exceptions import HTTPException

from forum.models.domain import Friendship
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
    for _id in [user_id, to_id]:
        user = await users.select_by_id(_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=strings.USER_NOT_FOUND
            )

    friendship = Friendship(first_id=user_id, second_id=to_id)
    ok = await friendships.insert(friendship)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=strings.ALREADY_FRIENDS
        )
