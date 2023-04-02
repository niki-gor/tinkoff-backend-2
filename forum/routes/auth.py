from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from forum.core.settings import AppSettings
from forum.dependencies.database import get_users_repo
from forum.dependencies.settings import get_app_settings
from forum.models.schemas import TokenInResponse, UserCredentials
from forum.repositories.base import BaseUsersRepository
from forum.resources import strings
from forum.services import jwt

router = APIRouter()


@router.post(
    "/login", response_model=TokenInResponse, status_code=status.HTTP_201_CREATED
)
async def login(
    credentials: UserCredentials,
    users: BaseUsersRepository = Depends(get_users_repo),
    settings: AppSettings = Depends(get_app_settings),
) -> TokenInResponse:
    wrong_id_or_password = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=strings.WRONG_ID_OR_PASSWD
    )
    user = await users.get_user_by_id(credentials.user_id)
    if user is None:
        raise wrong_id_or_password
    if not user.check_password(credentials.password):
        raise wrong_id_or_password

    token = jwt.create_access_token_for_user(
        user,
        str(settings.secret_key.get_secret_value()),
    )
    return TokenInResponse(token=token)
