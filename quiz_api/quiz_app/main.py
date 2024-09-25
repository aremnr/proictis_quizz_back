from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from quiz_app.routers import quiz, game, user, admin_side_html
from admin_side.main import router as admin_side_router

app = FastAPI(
    title="test",

)

app.include_router(quiz.router)
app.include_router(user.router)
app.include_router(game.router)
app.include_router(admin_side_router)
app.include_router(admin_side_html.router)
app.mount("/", StaticFiles(directory="/opt/app/static"), name="static")

