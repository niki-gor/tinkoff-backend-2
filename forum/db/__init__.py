from functools import lru_cache

from forum.db.models.memory import MemoryFriendshipManager, MemoryUserManager


@lru_cache
def users_table():
    return MemoryUserManager()


@lru_cache
def friendship_table():
    return MemoryFriendshipManager()
