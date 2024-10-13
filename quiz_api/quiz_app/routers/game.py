import uuid, json
from fastapi import APIRouter
from fastapi import Depends
import quiz_app.crud as crud
from sqlalchemy.orm import Session
from database.database import get_db
from admin_side.schemas import AdminSchema
from admin_side.admin_func import get_current_admin
from template.template_parser import get_game_html, get_admin_html, get_create_quiz, get_create_question
from fastapi.websockets import WebSocket, WebSocketDisconnect
from fastapi import Request
from fastapi.exceptions import HTTPException
from quiz_app.websocket_class import Game
from typing import Annotated

router = APIRouter()

games: dict[str, Game] = {}


@router.get("/create_game", tags=["game"])
async def create_game(quiz_id: str, admin: Annotated[AdminSchema, Depends(get_current_admin)]):
    game_id = str(uuid.uuid4())
    games[game_id] = Game(game_id = game_id, game_owner= admin.id, quiz_id=quiz_id)
    return {"game_id": game_id}


@router.get("/create_question")
def create_question(request: Request):
    return get_create_question(request=request)


@router.get("/create_quiz")
def create_quiz(request: Request):
    return get_create_quiz(request=request)


@router.get("/game/{game_id}", tags=["game"])
async def get_game(game_id: str, username: str, request: Request):
    return get_game_html(request=request)


@router.get("/admin_game/{game_id}", tags=["game"])
async def get_admin_game(game_id: str, admin: Annotated[AdminSchema, Depends(get_current_admin)], request: Request):
    return get_admin_html(request=request)


@router.websocket('/game/{game_id}')
async def game(websocket: WebSocket, game_id: str, db: Session = Depends(get_db)):

    game = games[game_id]
    await game.manager.connect(websocket)
    username: str = await websocket.receive_text()
    players = game.get_players()
    for player in players:
        await websocket.send_json({"header": "users", "username": player, "points": 0})
    try:
        admin: AdminSchema = await get_current_admin(username, db=db)
        game.add_admin(websocket=websocket, username=admin.username)
    except HTTPException:
        await game.add_player(websocket=websocket, username=username)
        await game.manager.JSON_broadcast({"header": "users", "username": username, "points": 0})
    try:
        while True:
            data = await websocket.receive_text()
            json_data = json.loads(data)
            if json_data['headers']['type'] == "game" and game.check_admin(websocket):
                game.question = crud.get_question(db=db, quiz_id=game.quiz_id, pcl=game.pcl)
                await game.manager.JSON_broadcast(json.loads(game.question.model_dump_json()))
                game.is_started = True
            if json_data['headers']['type'] == "check_answer" and game.is_started:
                if crud.check_answer(db=db, quiz_id=game.quiz_id, pcl=game.pcl, answer_plc=json_data['index']).is_right:
                    game.add_points(websocket=websocket, points_count=game.question.points)
                    await game.send_admins({'header': 'user_update', "username": game.users[websocket], "points": game.stats[game.users[websocket]]})
                if crud.get_quiz(db=db, quiz_id=game.quiz_id).question_count == game.pcl:
                    await websocket.send_text(f"end_game")
                else:
                    await game.manager.broadcast(f"empty_{game_id}")
            if json_data['headers']['type'] == "get_answer" and game.check_admin(websocket) and game.is_started:
                await websocket.send_json({"header": "Answer_check", f"Answer": crud.get_right_answer(db=db, quiz_id=game.quiz_id, pcl=game.pcl)})
                #await game.manager.broadcast(f"empty_{game_id}")
                game.pcl += 1
                if crud.get_quiz(db=db, quiz_id=game.quiz_id).question_count < game.pcl:
                    await game.send_admins({'header': 'end_game'})
                    await websocket.send_text(f"end_game")
                else:
                    await game.manager.broadcast(f"empty_{game_id}")
            if json_data['headers']['type'] == "end_game" and game.check_admin(websocket) and game.is_started:
                await game.send_admins({"header": "delete"})
                await websocket.send_text(f"results")
                stats = dict(sorted(game.stats.items(), key=lambda item: item[1], reverse=True))
                for username in stats.keys():
                    await game.manager.JSON_broadcast(
                        {"header": "users", "username": username, "points": game.stats[username]})
            else:
                pass
    except WebSocketDisconnect:
        game.manager.disconnect(websocket)

