from fastapi import FastAPI, HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse

from settings import app_settings
from src.admin_panel.admin_panel_routers import admin_panel_router
from src.auth.auth_handler import auth_handler
from src.auth.auth_routers import auth_router
from src.items.items_routers import items_router
from src.users.users_routers import users_router

app = FastAPI()

app.include_router(admin_panel_router)
app.include_router(items_router)
app.include_router(users_router)
app.include_router(auth_router)


@app.middleware("http")
async def check_login(request: Request, call_next):
    """" Для того, чтобы работать в админ-панели, нужно быть авторизованным админом.
     Поэтому проверяем наличие куки и валидность токена, в случае неудачи отправляем на логин. """

    url = request.url.path

    if url in app_settings.ALLOWED_URL:
        response = await call_next(request)
    else:
        try:
            token = request.cookies.get('admin_cookie')
            if not token:
                raise ValueError
            auth_handler.decode_token(token)
            response = await call_next(request)
            return response
        except (HTTPException, ValueError):
            response = RedirectResponse('/login', status_code=302)

    return response



