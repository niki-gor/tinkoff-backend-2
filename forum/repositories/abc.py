from abc import ABC, abstractmethod

from forum.models.domain import Friendship, User, UserInfo
from forum.models.schemas import UserInfoWithPassword


class BaseRepository(ABC):
    def __call__(self):
        return self


class BaseUserRepository(BaseRepository):
    @abstractmethod
    async def insert(self, user_info: UserInfoWithPassword) -> int:
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


class BaseFriendshipRepository(BaseRepository):
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
