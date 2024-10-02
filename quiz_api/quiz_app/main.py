from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from quiz_app.routers import quiz, game, user, admin_side_html
from admin_side.main import router as admin_side_router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(
    title="test",
)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(quiz.router)
app.include_router(user.router)
app.include_router(game.router)
app.include_router(admin_side_router)
app.include_router(admin_side_html.router)
app.mount("/static", StaticFiles(directory="template/static"), name="static")

