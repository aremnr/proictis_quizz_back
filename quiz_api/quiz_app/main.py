import quiz_app
from database.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, Request
import quiz_app.crud as crud
import quiz_app.schemas as schemas
from fastapi.responses import HTMLResponse
from template.template_parser import get_html_response, get_game_html
from fastapi.staticfiles import StaticFiles
from quiz_app.routers import quiz, game, user


app = FastAPI(
    title="test",

)

app.include_router(quiz.router)
app.include_router(user.router)
app.include_router(game.router)
app.mount("/static", StaticFiles(directory="template/static"), name="static")


@app.get("/get_html/{quiz_id}/{pcl}", response_class=HTMLResponse)
def get_html(request: Request, quiz_id: str, pcl: int, db: Session = Depends(get_db)):
    #return get_html_response(request=request, quiz_id=quiz_id, db=db, pcl=pcl)
    return get_game_html(request)

