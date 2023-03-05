from forum.repositories.memory import (MemoryFriendshipRepository,
                                     MemoryUserRepository)

users_repo = MemoryUserRepository()

friendships_repo = MemoryFriendshipRepository()
