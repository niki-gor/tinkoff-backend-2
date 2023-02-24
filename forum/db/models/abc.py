from abc import ABC, abstractmethod

from forum.api.models import User, UserInfo, Friendship


class BaseUserManager(ABC):
    @abstractmethod
    async def insert(self, ui: UserInfo) -> int:
        pass

    @abstractmethod
    async def select_all(self) -> list[User]:
        pass

    @abstractmethod
    async def select_by_id(self, user_id: int) -> User | None:
        pass

    @abstractmethod
    async def update(self, u: User) -> bool:
        pass


class BaseFriendshipManager(ABC):
    @abstractmethod
    async def insert(self, friendship: Friendship) -> bool:
        pass
