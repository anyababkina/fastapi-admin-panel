from fastapi import Request
from sqlalchemy.ext.asyncio import async_sessionmaker
from starlette.responses import RedirectResponse

from settings import app_settings
from src.models import User
from src.users.users_crud import UserQueryset
from src.users.users_schemas import UserSchema


async def user_table_view_services(
        request: Request,
        async_session_maker: async_sessionmaker,
        cselected_user: str
):
    """" Показ элементов таблицы в пользовательском интерфейсе в виде таблицы с записями. Логика фильтрации показа полей. """

    async with async_session_maker() as session:
        table_name = User.__name__
        columns = await UserQueryset.get_columns()
        # список столбцов, которые показываем в таблице (по умолчанию выбраны все)
        selected = cselected_user.split(",") if cselected_user else columns
        # выборка из таблицы, показывая только определенные столбцы
        records = await UserQueryset.get_multiple(session, selected)

        response = app_settings.TEMPLATES.TemplateResponse(
            'table_view.html',
            {
                'request': request,
                'table_name': table_name,
                'columns': columns,
                'selected': selected,
                'records': records
            }
        )

        # храним выбранные столбцы в куках (чтобы они сохранялись при обновлении страницы)
        response.set_cookie(key="cselected_user", value=",".join(selected))
        return response


async def user_update_cookie_services(checkbox: list):
    cselected_user = ','.join(checkbox)

    response = RedirectResponse('/user/instances', status_code=302)
    response.set_cookie(key="cselected_user", value=cselected_user)

    return response


async def user_instance_view_services(
        request: Request,
        instance_id: int,
        async_session_maker: async_sessionmaker,
        cselected_user: str
):
    """" Показ одного элемента. """

    async with async_session_maker() as session:
        table_name = User.__name__
        selected_columns = [c for c in await UserQueryset.get_columns() if c in cselected_user.split(',')]
        record = await UserQueryset.get_by_id(instance_id, session, selected_columns)

        return app_settings.TEMPLATES.TemplateResponse(
            'instance_view.html',
            {
                'request': request,
                'table_name': table_name,
                'columns': selected_columns,
                'record': record
            }
        )


async def user_create_page_services(
        request: Request,
):
    table_name = User.__name__
    columns = list(UserSchema.model_fields.keys())

    return app_settings.TEMPLATES.TemplateResponse(
        "creating_page.html",
        {
            "request": request,
            "table_name": table_name,
            "columns": columns
        }
    )


async def user_create_services(
        schema: UserSchema,
        async_session_maker: async_sessionmaker
):
    """" Создать user. """

    async with async_session_maker() as session:
        await UserQueryset.create(
            schema=schema,
            session=session
        )

    return RedirectResponse('/user/instances', status_code=302)


async def user_update_page_services(
        request: Request,
        instance_id: int,
        async_session_maker: async_sessionmaker
):
    """" Страница формы для редактирования текущего user."""

    async with async_session_maker() as session:
        table_name = User.__name__
        columns = list(UserSchema.model_fields.keys())
        curr_user = await UserQueryset.get_by_id(instance_id, session)

    return app_settings.TEMPLATES.TemplateResponse(
        "update_page.html",
        {
            "request": request,
            'table_name': table_name,
            'columns': columns,
            'record': curr_user
        }
    )


async def user_update_services(
        instance_id: int,
        schema: UserSchema,
        async_session_maker: async_sessionmaker
):
    """" POST-запрос на редактирование записи. """

    async with async_session_maker() as session:
        await UserQueryset.update(
            instance_id=instance_id,
            schema=schema,
            session=session
        )

    return RedirectResponse('/user/instances', status_code=302)


async def user_delete_services(
        instance_id: int,
        async_session_maker: async_sessionmaker,
):
    """" Удаление записи. """

    async with async_session_maker() as session:
        await UserQueryset.delete(
            instance_id=instance_id,
            session=session
        )

    return RedirectResponse('/user/instances', status_code=302)
