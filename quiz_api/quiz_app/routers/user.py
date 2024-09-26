from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, HTMLResponse
import quiz_app.schemas as schemas
from template.template_parser import get_user_html

router = APIRouter()


@router.get("/user_add/{game_id}", tags=["user"])
def user_add(game_id: str, request: Request):
    return get_user_html(request)

