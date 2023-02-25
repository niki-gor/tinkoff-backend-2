from fastapi import Depends, Query

from forum.db import users_table, friendship_table
from forum.db.models.abc import BaseUserManager, BaseFriendshipManager
from forum.api.models import Friendship, OkResponse, FriendshipRequest


async def befriend(
    from_id: int = Query(),
    to_id: int = Query(),
    users: BaseUserManager = Depends(users_table),
    friendships: BaseFriendshipManager = Depends(friendship_table),
) -> OkResponse:
    for user_id in [from_id, to_id]:
        user = await users.select_by_id(user_id)
        if user is None:
            return OkResponse(ok=False)
    friendship = Friendship(first_id=from_id, second_id=to_id)
    ok = await friendships.insert(friendship)
    return OkResponse(ok=ok)
