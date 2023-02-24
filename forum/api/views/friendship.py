from fastapi import Depends

from forum.db import users_table, friendship_table
from forum.db.models.abc import BaseUserManager, BaseFriendshipManager
from forum.api.models import Friendship, OkResponse


async def befriend(
    friendship: Friendship,
    users: BaseUserManager = Depends(users_table),
    friendships: BaseFriendshipManager = Depends(friendship_table),
) -> OkResponse:
    friends_ids = tuple([friendship.first_id, friendship.second_id])
    for user_id in friends_ids:
        user = await users.select_by_id(user_id)
        if user is None:
            return False
    ok = await friendships.insert(friends_ids)
    return OkResponse(ok=ok)
