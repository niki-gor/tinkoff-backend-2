from fastapi import Depends, Query, status, Response
from fastapi.responses import JSONResponse

from forum.db import users_table, friendship_table
from forum.db.models.abc import BaseUserManager, BaseFriendshipManager
from forum.api.models import Friendship


async def befriend(
    from_id: int = Query(),
    to_id: int = Query(),
    users: BaseUserManager = Depends(users_table),
    friendships: BaseFriendshipManager = Depends(friendship_table),
) -> Response:
    for user_id in [from_id, to_id]:
        user = await users.select_by_id(user_id)
        if user is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"detail": f"User with id {user_id} not found"}
            )
    friendship = Friendship(first_id=from_id, second_id=to_id)
    ok = await friendships.insert(friendship)
    if not ok:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Already friends"}
        )
    return Response(
        status_code=status.HTTP_201_CREATED
    )
