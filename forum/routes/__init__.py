from fastapi import APIRouter

from forum.routes import users, friends


router = APIRouter()
router.include_router(users.router, prefix='/users')
router.include_router(friends.router, prefix='/users/{user_id}/friends')