from typing import List

from websockets.exceptions import ConnectionClosedOK

from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from fastapi.encoders import jsonable_encoder

websocket_router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast_photo_action(self, message: dict):
        for con in self.active_connections:
            try:
                await con.send_json(jsonable_encoder(message))
            except WebSocketDisconnect:
                await self.disconnect(con)
            except ConnectionClosedOK:
                await self.disconnect(con)

ws_manager = ConnectionManager()

@websocket_router.websocket("/new_photos")
async def new_photos_websocket(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        print('ws errror')
        await ws_manager.disconnect(websocket)
