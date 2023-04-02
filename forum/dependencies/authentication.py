from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from forum.core.settings import AppSettings
from forum.dependencies.settings import get_app_settings
from forum.services import jwt


async def authenticate_user_id(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="/login")),
    settings: AppSettings = Depends(get_app_settings),
) -> int:
    return jwt.get_user_id_from_token(token, settings.secret_key.get_secret_value())
