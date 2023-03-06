from forum.models.domain import Friendship, User, UserInfo, UserInDB
from forum.models.schemas import UserInfoWithPlainPassword
from forum.repositories.abc import BaseFriendsRepository, BaseUsersRepository


class MemoryUsersRepository(BaseUsersRepository):
    def __init__(self):
        self.users: dict[int, UserInDB] = {}
        self.next_id = 1

    async def insert(self, user_info_passwd: UserInfoWithPlainPassword) -> int:
        self.users[self.next_id] = UserInDB(
            **user_info_passwd.dict(),
            user_id=self.next_id,
        )
        self.users[self.next_id].change_password(user_info_passwd.password)
        try:
            return self.next_id
        finally:
            self.next_id += 1

    async def select_all(self) -> list[User]:
        return [
            User(**user_with_passwd.dict()) for user_with_passwd in self.users.values()
        ]

    async def select_by_id(self, user_id: int) -> UserInfo | None:
        try:
            user_with_passwd = self.users[user_id]
        except KeyError:
            return None
        return UserInfo(**user_with_passwd.dict())

    async def update(self, user_id: int, user_info: UserInfo) -> bool:
        try:
            user2update = self.users[user_id]
        except KeyError:
            return False
        # NB: user2update = ...  will not update self.users dict
        self.users[user_id] = user2update.copy(update=user_info.dict())
        return True


class MemoryFriendsRepository(BaseFriendsRepository):
    def __init__(self):
        self.friendships: set[tuple] = set()

    async def insert(self, first_id: int, second_id: int) -> bool:
        friends = tuple([first_id, second_id])
        if friends in self.friendships:
            return False
        self.friendships.add(friends)
        return True
