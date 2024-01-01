from sqlalchemy.ext.asyncio import async_sessionmaker
from starlette.requests import Request
from starlette.responses import RedirectResponse

from settings import app_settings
from src.auth.auth_crud import AdminQueryset
from src.auth.auth_handler import auth_handler
from src.models import Base
from src.admin_panel.admin_panel_crud import Queryset


async def main_page_services(
        request: Request,
        async_session_maker: async_sessionmaker,
):
    """" Главная страница админки, где дашборд с общим количеством элементов в каждой доступной в бд таблице. """

    dashboard = {}

    try:
        cookie = request.cookies.get('admin_cookie')
        admin_id = auth_handler.decode_token(cookie)

    except:
        response = RedirectResponse('/login', status_code=302)
        return response

    async with async_session_maker() as session:
        admin = await AdminQueryset.get_by_id(admin_id, session)

        model_classes = {
            model_name: model_class for model_name, model_class in Base.registry._class_registry.items()
            if model_name != 'Admin' and not model_name.startswith('_')
    }

        for model_name, model_class in model_classes.items():
            queryset = Queryset(model_class)
            count = await queryset.count(session)
            dashboard[model_name] = count

    return app_settings.TEMPLATES.TemplateResponse(
        'main_page.html',
        {
            'request': request,
            'admin': admin,
            'dashboard': dashboard
        }
    )
