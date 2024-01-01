from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse

from dependency import SessionMakerDep
from src.admin_panel.admin_panel_services import main_page_services

admin_panel_router = APIRouter(prefix='', tags=['admin_panel'])


@admin_panel_router.get('/', response_class=HTMLResponse, description='Страница с дашбордами')
async def main_page(
        request: Request,
        async_session_maker: SessionMakerDep,
):
    response = await main_page_services(
        request=request,
        async_session_maker=async_session_maker
    )

    return response