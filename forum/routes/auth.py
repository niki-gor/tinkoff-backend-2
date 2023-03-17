from fastapi import APIRouter, Depends, Response, status
from fastapi.exceptions import HTTPException
from forum.core.config import AppSettings
from forum.models.domain import User

from forum.models.schemas import (
    ListOfUsersInResponse,
    TokenInResponse,
    UserCredentials,
    UserIdInResponse,
    UserInResponse,
    UserInUpdate,
    JWTUser,
    UserInCreate,
    UserWithToken,
)
from forum.dependencies.database import users_repo
from forum.repositories.base import BaseUsersRepository
from forum.resources import strings
from forum.services import jwt
from forum.core.config import app_settings, AppSettings

router = APIRouter()


@router.post("/login", response_model=TokenInResponse)
async def login(
    credentials: UserCredentials,
    users: BaseUsersRepository = Depends(users_repo),
    settings: AppSettings = Depends(app_settings),
) -> TokenInResponse:
    wrong_id_or_password = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=strings.WRONG_ID_OR_PASSWD
    )
    user = await users.select_by_id(credentials.user_id)
    if user is None:
        raise wrong_id_or_password
    if not user.check_password(credentials.password):
        raise wrong_id_or_password
    
    token = jwt.create_access_token_for_user(
        user,
        str(settings.secret_key.get_secret_value()),
    )
    return TokenInResponse(token=token)
