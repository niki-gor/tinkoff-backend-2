from fastapi import APIRouter

from forum.api.routes import ROUTES

router = APIRouter(routes=ROUTES)
