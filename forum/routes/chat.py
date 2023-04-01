from typing import List

from fastapi import (APIRouter, Depends, HTTPException, Request, WebSocket,
                     WebSocketDisconnect, status)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from forum.dependencies.authentication import authenticate_user_id
from forum.dependencies.database import get_friends_repo
from forum.repositories.base import BaseFriendsRepository
from forum.resources import strings

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()
templates = Jinja2Templates(directory="templates")


@router.get("/users/{user_id}/chat/{to_id}", response_class=HTMLResponse)
async def get_chat(
    request: Request,
    user_id: int,
    to_id: int,
    auth_user_id: int = Depends(authenticate_user_id),
    friends: BaseFriendsRepository = Depends(get_friends_repo),
):
    if user_id != auth_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.INSUFFICIENT_PERMISSIONS,
        )

    are_friends = await friends.are_friends(user_id, to_id)
    if not are_friends:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.CHAT_ONLY_FRIENDS,
        )

    return templates.TemplateResponse(
        "chat.html", {"request": request, "client_id": user_id}
    )


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
