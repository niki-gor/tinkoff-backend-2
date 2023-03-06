from datetime import datetime

from pydantic import BaseModel

from forum.models.domain import User, UserInfo


class UserIdInResponse(BaseModel):
    user_id: int


class ListOfUsersInResponse(BaseModel):
    users: list[User]


class UserInfoInResponse(BaseModel):
    user_info: UserInfo


class JWTMeta(BaseModel):
    exp: datetime
    sub: str


class JWTUser(BaseModel):
    username: str


class UserInfoWithPlainPassword(UserInfo):
    password: str
    