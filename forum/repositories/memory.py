from forum.models.domain import User, UserInDB
from forum.repositories.abc import BaseFriendsRepository, BaseUsersRepository


class MemoryUsersRepository(BaseUsersRepository):
    def __init__(self):
        self.users: dict[int, UserInDB] = {}
        self.next_id = 1

    async def insert(
        self, *, name: str, about: str, age: int, email: str, password: str
    ) -> int:
        user = UserInDB(
            user_id=self.next_id, name=name, about=about, age=age, email=email
        )
        user.change_password(password)
        self.users[self.next_id] = user
        try:
            return self.next_id
        finally:
            self.next_id += 1

    async def select_all(self) -> list[User]:
        return [
            User(**user_with_passwd.dict()) for user_with_passwd in self.users.values()
        ]

    async def select_by_id(self, user_id: int) -> User | None:
        try:
            user_with_passwd = self.users[user_id]
        except KeyError:
            return None
        return User(**user_with_passwd.dict())

    async def update(
        self,
        *,
        user_id: int,
        name: str | None = None,
        about: str | None = None,
        age: int | None = None,
        email: str | None = None,
        password: str | None = None
    ) -> bool:
        try:
            updated_user = self.users[user_id]
        except KeyError:
            return False
        updated_user.name = name or updated_user.name
        updated_user.about = about or updated_user.about
        updated_user.age = age or updated_user.age
        updated_user.email = email or updated_user.email
        if password:
            updated_user.change_password(password)

        # NB: user2update = ...  will not update self.users dict
        self.users[user_id] = updated_user
        return True


class MemoryFriendsRepository(BaseFriendsRepository):
    def __init__(self):
        self.friendships: set[tuple] = set()

    async def insert(self, from_id: int, to_id: int) -> bool:
        friendship = tuple([from_id, to_id])
        if friendship in self.friendships:
            return False
        self.friendships.add(friendship)
        return True
