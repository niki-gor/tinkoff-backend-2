from typing import AsyncGenerator

from asyncpg import Connection, Pool
from fastapi import Depends, Request
from forum.repositories.base import BaseFriendsRepository, BaseUsersRepository
from forum.repositories.database import DatabaseFriendsRepository, DatabaseUsersRepository


def get_db_pool(request: Request) -> Pool:
    return request.app.state.pool


async def get_connection_from_pool(
    pool: Pool = Depends(get_db_pool),
) -> AsyncGenerator[Connection, None]:
    async with pool.acquire() as conn:
        yield conn


def get_users_repo(conn: Connection = Depends(get_connection_from_pool)):
    return DatabaseUsersRepository(conn)


def get_friends_repo(conn: Connection = Depends(get_connection_from_pool)):
    return DatabaseFriendsRepository(conn)

# @lru_cache
# def get_friends_repo():
#     return MemoryFriendsRepository()


# def get_repository(
#     repo_type: Type[BaseRepository],
# ) -> Callable[[Connection], BaseRepository]:
#     def _get_repo(
#         conn: Connection = Depends(_get_connection_from_pool),
#     ) -> BaseRepository:
#         return repo_type(conn)

#     return _get_repo
