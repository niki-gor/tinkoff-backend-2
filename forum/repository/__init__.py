from functools import lru_cache

from forum.repository.memory import MemoryFriendshipRepository, MemoryUserRepository


@lru_cache
def users_table():
    return MemoryUserRepository()


@lru_cache
def friendship_table():
    return MemoryFriendshipRepository()
