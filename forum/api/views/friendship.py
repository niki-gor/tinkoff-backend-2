from fastapi import Depends, status, Response

from forum.repository import users_table, friendship_table
from forum.repository.abc import BaseUserRepository, BaseFriendshipRepository
from forum.api.models import Friendship, EmptyBody, Error


async def befriend(
    from_id: int,
    to_id: int,
    r: Response,
    users: BaseUserRepository = Depends(users_table),
    friendships: BaseFriendshipRepository = Depends(friendship_table),
) -> Error | EmptyBody:
    for user_id in [from_id, to_id]:
        user = await users.select_by_id(user_id)
        if user is None:
            r.status_code = status.HTTP_404_NOT_FOUND
            return Error(detail=f"User with id {user_id} not found")

    friendship = Friendship(first_id=from_id, second_id=to_id)
    ok = await friendships.insert(friendship)
    if not ok:
        r.status_code = status.HTTP_400_BAD_REQUEST
        return Error(detail="Already friends")

    r.status_code = status.HTTP_201_CREATED
    return {}
