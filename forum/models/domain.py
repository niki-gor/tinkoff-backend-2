from pydantic import BaseModel, root_validator, validator, EmailStr
from forum.services import security


class UserInfo(BaseModel):
    name: str
    about: str
    age: int
    email: EmailStr

    @validator("name")
    def name_exists_not_too_long(cls, v):
        if not 1 <= len(v) <= 30:
            raise ValueError("invalid name length")
        return v

    @validator("about")
    def about_not_too_long(cls, v):
        if not len(v) <= 120:
            raise ValueError("too much info about you")
        return v

    @validator("age")
    def age_i_can_believe(cls, v):
        if not 1 <= v <= 120:
            raise ValueError("I don't believe you")
        return v


class User(UserInfo):
    user_id: int


class UserInDB(User):
    hashed_password: str = ""

    def check_password(self, plain_password: str) -> bool:
        return security.verify_password(plain_password, self.hashed_password)
    
    def change_password(self, plain_password: str):
        return security.get_password_hash(plain_password)
