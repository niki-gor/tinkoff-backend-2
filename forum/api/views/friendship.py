from fastapi import Depends, Response, status

from forum.api.errors import ErrAlreadyFriends, ErrUserNotFound
from forum.api.models import EmptyBody, Error, Friendship
from forum.repository import friendships_repo, users_repo
from forum.repository.abc import BaseFriendshipRepository, BaseUserRepository


async def befriend(
    from_id: int,
    to_id: int,
    r: Response,
    users: BaseUserRepository = Depends(users_repo),
    friendships: BaseFriendshipRepository = Depends(friendships_repo),
) -> Error | EmptyBody:
    for user_id in [from_id, to_id]:
        user = await users.select_by_id(user_id)
        if user is None:
            r.status_code = status.HTTP_404_NOT_FOUND
            return ErrUserNotFound

    friendship = Friendship(first_id=from_id, second_id=to_id)
    ok = await friendships.insert(friendship)
    if not ok:
        r.status_code = status.HTTP_400_BAD_REQUEST
        return ErrAlreadyFriends

    r.status_code = status.HTTP_201_CREATED
    return {}
