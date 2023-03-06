from forum.models.domain import Friendship, User, UserInfo
from forum.models.schemas import UserInfoWithPassword
from forum.repositories.abc import BaseFriendshipRepository, BaseUserRepository


class MemoryUserRepository(BaseUserRepository):
    def __init__(self):
        self.users: dict[int, UserInfo] = {}
        self.next_id = 1

    async def insert(self, user_info: UserInfoWithPassword) -> int:
        self.users[self.next_id] = user_info
        try:
            return self.next_id
        finally:
            self.next_id += 1

    async def select_all(self) -> list[User]:
        return [
            User(user_id=user_id, **user_info.dict())
            for user_id, user_info in self.users.items()
        ]

    async def select_by_id(self, user_id: int) -> UserInfo | None:
        return self.users.get(user_id)

    async def update(self, user_id: int, user_info: UserInfo) -> bool:
        if user_id not in self.users:
            return False
        self.users[user_id] = user_info
        return True


class MemoryFriendshipRepository(BaseFriendshipRepository):
    def __init__(self):
        self.friendships: set[tuple] = set()

    async def insert(self, friendship: Friendship) -> bool:
        if tuple(friendship) in self.friendships:
            return False
        self.friendships.add(tuple(friendship))
        return True
