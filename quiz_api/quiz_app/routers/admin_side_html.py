from template.template_parser import get_admin_login_html, get_admin_registration_html, get_profile_html
from fastapi import APIRouter, Depends, Request
from admin_side.admin_func import get_current_admin
from admin_side.schemas import AdminSchema
from typing import Annotated


router = APIRouter()


@router.get('/log', tags=["auth"])
async def get_log(request: Request):
    return get_admin_login_html(request)


@router.get('/registration', tags=["auth"])
async def get_registration(request: Request):
    return get_admin_registration_html(request)


@router.get('/profile', tags=["auth"])
async def get_profile(request: Request):
    return get_profile_html(request)

