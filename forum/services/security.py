import logging
import bcrypt

PEPPER = "LOL"


def make_peppered(plain_password: str):
    return plain_password + PEPPER


def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    peppered_password = make_peppered(plain_password)
    return bcrypt.checkpw(peppered_password.encode(), hashed_password)


def get_password_hash(plain_password: str) -> bytes:
    peppered_password = make_peppered(plain_password)
    salt = bcrypt.gensalt(rounds=5)
    hashed_password = bcrypt.hashpw(peppered_password.encode(), salt)
    return hashed_password
