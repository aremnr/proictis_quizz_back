from fastapi import WebSocket
from quiz_app import crud
from sqlalchemy.orm import Session

from quiz_app.schemas import Question


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def JSON_broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)


class Game:
    def __init__(self, game_id: str, game_owner: str, quiz_id: str):
        self.game_id: str = game_id
        self.game_owner: str = game_owner
        self.quiz_id: str = quiz_id
        self.manager = ConnectionManager()
        self.stats: dict[str, int] = {}
        self.users: dict[WebSocket, str] = {}
        self.pcl: int = 1
        self.admins: dict[WebSocket, str] = {}
        self.is_started: bool = False
        self.question: Question

    async def add_player(self, username: str, websocket: WebSocket):
        if username not in self.users:
            self.stats[username] = 0
            self.users[websocket] = username
            return True
        return False

    def get_players(self):
        return list(self.stats.keys())

    def add_admin(self, username: str, websocket: WebSocket):
        self.admins[websocket] = username

    def add_points(self, points_count: int, websocket: WebSocket):
        self.stats[self.users[websocket]] += points_count

    async def send_admins(self, message: dict):
        for admin in self.admins.keys():
            await admin.send_json(message)
