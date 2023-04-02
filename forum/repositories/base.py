from abc import ABC, abstractmethod

from forum.models.domain import User, UserInDB


class BaseUsersRepository(ABC):
    @abstractmethod
    async def create_user(
        self, *, name: str, about: str, age: int, email: str, password: str
    ) -> int:
        pass

    @abstractmethod
    async def get_all_users(self) -> list[User]:
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> UserInDB | None:
        pass

    @abstractmethod
    async def update_user_by_id(
        self,
        *,
        user_id: int,
        name: str,
        about: str,
        age: int,
        email: str,
        password: str
    ) -> bool:
        pass


class BaseFriendsRepository(ABC):
    @abstractmethod
    async def create_friends(self, from_id: int, to_id: int) -> bool:
        pass

    @abstractmethod
    async def are_friends(self, first_id: int, second_id: int) -> bool:
        pass
