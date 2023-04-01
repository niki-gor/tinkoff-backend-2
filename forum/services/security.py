import bcrypt

from forum.dependencies.settings import get_app_settings


def make_peppered(plain_password: str):
    settings = get_app_settings()
    pepper = settings.secret_key
    return plain_password + pepper


def verify_password(plain_password: str, hashed_password: str) -> bool:
    peppered_password = make_peppered(plain_password)
    return bcrypt.checkpw(peppered_password.encode(), hashed_password.encode())


def get_password_hash(plain_password: str) -> str:
    peppered_password = make_peppered(plain_password)
    salt = bcrypt.gensalt(rounds=5)
    hashed_password = bcrypt.hashpw(peppered_password.encode(), salt)
    return hashed_password.decode()
