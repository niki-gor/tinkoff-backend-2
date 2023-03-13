from abc import ABC, abstractmethod

from forum.models.domain import User


class BaseRepository(ABC):
    def __call__(self):
        return self


class BaseUsersRepository(BaseRepository):
    @abstractmethod
    async def insert(
        self, *, name: str, about: str, age: int, email: str, password: str
    ) -> int:
        pass

    @abstractmethod
    async def select_all(self) -> list[User]:
        pass

    @abstractmethod
    async def select_by_id(self, user_id: int) -> User | None:
        pass

    @abstractmethod
    async def update(
        self, *, user_id: int, name: str, about: str, age: int, email: str, password: str
    ) -> bool:
        pass


class BaseFriendsRepository(BaseRepository):
    @abstractmethod
    async def insert(self, from_id: int, to_id: int) -> bool:
        pass


# class BasePasswordRepository(BaseRepository):
#     def __init__(self, encrypter)

#     @abstractmethod
#     async def insert(self, user_id: int, password: str) -> bool:
#         pass

#     @abstractmethod
#     async def select(self, user_id: int, password: str) -> bool:
#         pass
