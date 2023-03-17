from pydantic import BaseModel
from forum.services import security


class User(BaseModel):
    user_id: int
    name: str
    about: str
    age: int
    email: str


class UserInDB(User):
    hashed_password: bytes = ''.encode()

    def check_password(self, plain_password: str) -> bool:
        return security.verify_password(plain_password, self.hashed_password)
    
    def change_password(self, plain_password: str):
        self.hashed_password = security.get_password_hash(plain_password)
