from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from dependency import SessionMakerDep
from settings import app_settings
from src.auth.auth_schemas import AdminRegistration, AdminLogin
from src.auth.auth_services import registration_services, login_services, logout_services


auth_router = APIRouter(prefix='', tags=['admin_auth'])

# регистрация и авторизация


@auth_router.get('/registration', response_class=HTMLResponse)
async def registration_page(request: Request):
    return app_settings.TEMPLATES.TemplateResponse("registry.html", {"request": request})


@auth_router.post('/registration', response_class=HTMLResponse)
async def registration(
        async_session_maker: SessionMakerDep,
        schema: Annotated[AdminRegistration, Depends(AdminRegistration.as_form)]
):
    response = await registration_services(
        schema=schema,
        async_session_maker=async_session_maker
    )

    return response


@auth_router.get('/login', response_class=HTMLResponse)
async def login_page(request: Request):
    return app_settings.TEMPLATES.TemplateResponse("login.html", {"request": request})


@auth_router.post('/login', response_class=HTMLResponse)
async def login(
        async_session_maker: SessionMakerDep,
        schema: Annotated[AdminLogin, Depends(AdminLogin.as_form)]
):
    response = await login_services(
        schema=schema,
        async_session_maker=async_session_maker
    )

    return response


@auth_router.get('/logout', response_class=RedirectResponse)
async def logout():
    response = await logout_services()

    return response