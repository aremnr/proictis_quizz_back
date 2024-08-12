from fastapi import Request
from fastapi.templating import Jinja2Templates
import quiz_app.crud as crud
import quiz_app.schemas as schemas
templates = Jinja2Templates(directory="template")

def get_game_html(request: Request):
    html_data = templates.TemplateResponse(request=request, name="game.html", context={})
    return html_data


def get_admin_html(request: Request):
    html_data = templates.TemplateResponse(request=request, name="admin.game.html", context={})
    return html_data


def get_user_html(request: Request):
    html_data = templates.TemplateResponse(request=request, name="user_add.html", context={})
    return html_data

def get_admin_registration_html(request: Request):
    html_data = templates.TemplateResponse(request=request, name="admin_register.html", context={})
    return html_data

def get_admin_login_html(request: Request):
    html_data = templates.TemplateResponse(request=request, name="admin_login.html", context={})
    return html_data

def get_profile_html(request: Request):
    html_data = templates.TemplateResponse(request=request, name="profile.html", context={})
    return html_data