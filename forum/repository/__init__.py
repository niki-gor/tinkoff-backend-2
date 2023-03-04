from functools import lru_cache

from forum.repository.memory import MemoryFriendshipRepository, MemoryUserRepository


_users_repo = MemoryUserRepository()
users_repo = lambda: _users_repo

_friendships_repo = MemoryFriendshipRepository()
friendships_repo = lambda: _friendships_repo
