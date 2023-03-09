from abc import ABC, abstractmethod

from forum.models.domain import Friendship, User, UserInfo
from forum.models.schemas import UserInfoWithPlainPassword


class BaseRepository(ABC):
    def __call__(self):
        return self


class BaseUsersRepository(BaseRepository):
    @abstractmethod
    async def insert(self, user_info: UserInfoWithPlainPassword) -> int:
        pass

    @abstractmethod
    async def select_all(self) -> list[User]:
        pass

    @abstractmethod
    async def select_by_id(self, user_id: int) -> UserInfo | None:
        pass

    @abstractmethod
    async def update(self, user_id: int, user_info: UserInfo) -> bool:
        pass


class BaseFriendsRepository(BaseRepository):
    @abstractmethod
    async def insert(self, friendship: Friendship) -> bool:
        pass


# class BasePasswordRepository(BaseRepository):
#     def __init__(self, encrypter)

#     @abstractmethod
#     async def insert(self, user_id: int, password: str) -> bool:
#         pass

#     @abstractmethod
#     async def select(self, user_id: int, password: str) -> bool:
#         pass
