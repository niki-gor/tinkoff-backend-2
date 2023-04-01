import pytest
from fastapi.testclient import TestClient

from forum import get_application
from forum.dependencies.database import get_connection_from_pool
from forum.models.domain import User
from forum.models.schemas import UserCredentials, UserInCreate

app = get_application()
client = TestClient(app)
user_mock = User(
    user_id=-1,
    name="lol",
    about="literally nothing",
    age=42,
    email="lol@example.com",
)
user_mock_passwd = UserInCreate(**user_mock.dict(), password="123QQQqqq")


@pytest.fixture
async def new_app():
    async with get_connection_from_pool() as conn:
        await conn.execute(
            """
            truncate table friends;
            truncate table users;
        """
        )
    yield app


def get_authorization_headers(*, user_id: int) -> dict:
    response = client.post(
        "/login",
        json=UserCredentials(**user_mock_passwd.dict(), user_id=user_id).dict(),
    )
    token = response.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    return headers
