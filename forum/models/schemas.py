from datetime import datetime

from pydantic import BaseModel, EmailStr, validator

from forum.models.domain import User
from forum.models import validators


class UserInLogin(BaseModel):
    user_id: int
    password: str

class UserIdInResponse(BaseModel):
    user_id: int


class ListOfUsersInResponse(BaseModel):
    users: list[User]


class UserInResponse(BaseModel):
    user: User


class UserCredentials(BaseModel):
    user_id: int
    password: str


class JWTMeta(BaseModel):
    exp: datetime
    sub: str


class JWTUser(BaseModel):
    user_id: int


class UserInCreate(BaseModel):
    name: str
    about: str
    age: int
    email: EmailStr
    password: str

    @validator("name")
    def name_exists_not_too_long(cls, v):
        return validators.name_exists_not_too_long(v)

    @validator("about")
    def about_not_too_long(cls, v):
        return validators.about_not_too_long(v)

    @validator("age")
    def age_i_can_believe(cls, v):
        return validators.age_i_can_believe(v)
    
    @validator("password")
    def good_password(cls, v: str):
        return validators.good_password(v)


class UserInUpdate(BaseModel):
    name: str | None = None
    about: str | None = None
    age: int | None = None
    email: EmailStr | None = None
    password: str | None = None

    @validator("name")
    def name_exists_not_too_long(cls, v):
        return validators.name_exists_not_too_long(v)

    @validator("about")
    def about_not_too_long(cls, v):
        return validators.about_not_too_long(v)

    @validator("age")
    def age_i_can_believe(cls, v):
        return validators.age_i_can_believe(v)
    
    @validator("password")
    def good_password(cls, v: str):
        return validators.good_password(v)