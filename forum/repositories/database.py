from datetime import datetime
from asyncpg import Connection
import asyncpg

from forum.db.queries import queries
from forum.models.domain import User, UserInDB
from forum.repositories.base import BaseFriendsRepository, BaseUsersRepository
from forum.resources import strings


class DatabaseUsersRepository(BaseUsersRepository):
    def __init__(self, conn: Connection):
        self.conn = conn

    async def create_user(
        self, *, name: str, about: str, age: int, email: str, password: str, last_login_at: str
    ) -> int:
        user = UserInDB(user_id=0, name=name, about=about, age=age, email=email, last_login_at=last_login_at)
        user.change_password(password)
        user_id = await queries.create_user(
            self.conn,
            name=user.name,
            about=user.about,
            age=user.age,
            email=user.email,
            hashed_password=user.hashed_password,
            last_login_at=user.last_login_at
        )
        return user_id

    async def get_all_users(self) -> list[User]:
        users_rows = await queries.get_all_users(self.conn)
        users = [User(**row) for row in users_rows]
        return users

    async def get_user_by_id(self, user_id: int) -> UserInDB | None:
        user_row = await queries.get_user_by_id(self.conn, user_id)
        if user_row is None:
            return None
        return UserInDB(**user_row)

    async def update_user_by_id(
        self,
        *,
        user_id: int,
        name: str | None = None,
        about: str | None = None,
        age: int | None = None,
        email: str | None = None,
        password: str | None = None,
        last_login_at: str | None = None
    ) -> bool:
        user = await queries.get_user_by_id(self.conn, user_id)
        if user is None:
            return False
        updated_user = UserInDB(**user)
        updated_user.name = name or updated_user.name
        updated_user.about = about or updated_user.about
        updated_user.age = age or updated_user.age
        updated_user.email = email or updated_user.email
        if password:
            updated_user.change_password(password)
        updated_user.last_login_at = last_login_at or updated_user.last_login_at
        await queries.update_user_by_id(self.conn, **updated_user.dict())
        return True


class DatabaseFriendsRepository(BaseFriendsRepository):
    def __init__(self, conn: Connection):
        self.conn = conn

    async def create_friends(self, from_id: int, to_id: int):
        try:
            created = await queries.create_friends(self.conn, from_id=from_id, to_id=to_id)
            if not created:
                now = datetime.now().isoformat()
                updated = await queries.accept_friends(self.conn, from_id=from_id, to_id=to_id, accepted_at=now)
                if not updated:
                    raise ValueError(strings.ALREADY_FRIENDS)
        except asyncpg.exceptions.UniqueViolationError:
            raise ValueError(strings.ALREADY_FRIENDS)
        except asyncpg.exceptions.ForeignKeyViolationError:
            raise ValueError(strings.USER_NOT_FOUND)

    async def are_friends(self, first_id: int, second_id: int) -> bool:
        indeed = await queries.are_friends(
            self.conn, first_id=first_id, second_id=second_id
        )
        return indeed
