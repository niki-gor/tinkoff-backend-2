from pydantic import BaseModel, EmailStr, root_validator, validator


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


class UserId(BaseModel):
    user_id: int


class Error(BaseModel):
    detail: str


class EmptyBody(BaseModel):
    '''
    NB: EmptyBody всегда должен стоять в конце перечислений Type1 | ... | TypeN | EmptyBody.
    Тело пустое => EmptyBody соответствует любой словарь. 
    Из-за механики работы Pydantic, все словари из-за этого кастятся к EmptyBody — пустому словарю
    '''
    pass


class Friendship(BaseModel):
    first_id: int
    second_id: int

    @validator("first_id", "second_id")
    def id_is_ok(cls, v):
        if v < 0:
            raise ValueError("expected user_id > 0")
        return v

    @root_validator
    def first_not_eq_second(cls, values):
        if values["first_id"] == values["second_id"]:
            raise ValueError("friends IDs should be different")
        return values
    
    @root_validator
    def make_sorted(cls, values):
        values["first_id"], values["second_id"] = sorted([values["first_id"], values["second_id"]])
        return values
        