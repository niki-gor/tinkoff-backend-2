from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import decode, exceptions, encode

from forum.services import jwt
from forum.core.config import AppSettings, app_settings


async def authenticate_user_id( 
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="/login")),
    settings: AppSettings = Depends(app_settings)
) -> int:
    return jwt.get_user_id_from_token(token, settings.secret_key.get_secret_value())
