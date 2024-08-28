from utils.websocket import *
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.helpers.custom_exception_handler import *

router = APIRouter()

@router.websocket("/notifications")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)