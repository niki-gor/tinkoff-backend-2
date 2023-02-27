from abc import ABC, abstractmethod

from forum.api.models import User, UserInfo, Friendship


class BaseUserRepository(ABC):
    @abstractmethod
    async def insert(self, user_info: UserInfo) -> int:
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


class BaseFriendshipRepository(ABC):
    @abstractmethod
    async def insert(self, friendship: Friendship) -> bool:
        pass
