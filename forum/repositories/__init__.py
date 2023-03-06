from forum.repositories.memory import (MemoryFriendsRepository,
                                     MemoryUsersRepository)

users_repo = MemoryUsersRepository()

friendships_repo = MemoryFriendsRepository()
