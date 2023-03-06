from forum.models.domain import Friendship, User, UserInfo
from forum.models.schemas import UserInfoWithPassword
from forum.repositories.abc import BaseFriendshipRepository, BaseUserRepository


class MemoryUserRepository(BaseUserRepository):
    def __init__(self):
        self.users: dict[int, UserInfoWithPassword] = {}
        self.next_id = 1

    async def insert(self, user_info_passwd: UserInfoWithPassword) -> int:
        self.users[self.next_id] = user_info_passwd
        try:
            return self.next_id
        finally:
            self.next_id += 1

    async def select_all(self) -> list[User]:
        return [
            User(user_id=user_id, **user_info_passwd.dict())
            for user_id, user_info_passwd in self.users.items()
        ]

    async def select_by_id(self, user_id: int) -> UserInfo | None:
        return self.users.get(user_id)

    async def update(self, user_id: int, user_info: UserInfo) -> bool:
        try:
            user2update = self.users[user_id]
        except KeyError:
            return False
        self.users[user_id] = user2update.copy(update=user_info.dict())
        return True


class MemoryFriendshipRepository(BaseFriendshipRepository):
    def __init__(self):
        self.friendships: set[tuple] = set()

    async def insert(self, friendship: Friendship) -> bool:
        if tuple(friendship) in self.friendships:
            return False
        self.friendships.add(tuple(friendship))
        return True
