from fastapi import APIRouter

from forum.routes import friends, users, auth, chat

router = APIRouter()
router.include_router(users.router, prefix="/users")
router.include_router(friends.router, prefix="/users/{user_id}/friends")
router.include_router(auth.router)
router.include_router(chat.router)
