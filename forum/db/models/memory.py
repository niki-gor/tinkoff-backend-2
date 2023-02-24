from forum.api.models import User, UserInfo, Friendship
from forum.db.models.abc import BaseFriendshipManager, BaseUserManager


class MemoryUserManager(BaseUserManager):
    def __init__(self):
        self.users: dict[int, User] = {}
        self.next_id = 1

    async def insert(self, ui: UserInfo) -> int:
        self.users[self.next_id] = User(**ui.dict(), user_id=self.next_id)
        try:
            return self.next_id
        finally:
            self.next_id += 1

    async def select_all(self) -> list[User]:
        return list(self.users.values())

    async def select_by_id(self, user_id: int) -> User | None:
        return self.users.get(user_id)

    async def update(self, u: User) -> bool:
        if u.user_id not in self.users:
            return False
        self.users[u.user_id] = u
        return True


class MemoryFriendshipManager(BaseFriendshipManager):
    def __init__(self):
        self.friendships: set[tuple] = set()

    async def insert(self, friendship: Friendship) -> bool:
        if tuple(friendship) in self.friendships:
            return False
        self.friendships.add(tuple(friendship))
        return True
