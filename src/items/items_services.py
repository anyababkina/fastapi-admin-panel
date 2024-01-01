from fastapi import Request, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker
from starlette.responses import RedirectResponse

from settings import app_settings
from src.items.items_crud import ItemQueryset
from src.items.items_schemas import ItemSchema
from src.models import Item


async def item_table_view_services(
        request: Request,
        async_session_maker: async_sessionmaker,
        cselected_item: str
):
    """" Показ элементов таблицы в пользовательском интерфейсе в виде таблицы с записями. Логика фильтрации показа полей. """

    async with async_session_maker() as session:
        table_name = Item.__name__
        columns = await ItemQueryset.get_columns()
        # список столбцов, которые показываем в таблице (по умолчанию выбраны все)
        selected = cselected_item.split(",") if cselected_item else columns
        # выборка из таблицы, показывая только определенные столбцы
        records = await ItemQueryset.get_multiple(session, selected)

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
        response.set_cookie(key="cselected_item", value=",".join(selected))
        return response


async def item_update_cookie_services(checkbox: list):
    cselected_item = ','.join(checkbox)

    response = RedirectResponse('/item/instances', status_code=302)
    response.set_cookie(key="cselected_item", value=cselected_item)

    return response


async def item_instance_view_services(
        request: Request,
        instance_id: int,
        async_session_maker: async_sessionmaker,
        cselected_item: str
):
    """" Показ одного элемента с учетом фильтров колонок на главной странице таблицы """

    async with async_session_maker() as session:
        table_name = Item.__name__
        selected_columns = [c for c in await ItemQueryset.get_columns() if c in cselected_item.split(',')]
        record = await ItemQueryset.get_by_id(instance_id, session, selected_columns)

        return app_settings.TEMPLATES.TemplateResponse(
            'instance_view.html',
            {
                'request': request,
                'table_name': table_name,
                'columns': selected_columns,
                'record': record
            }
        )


async def item_create_page_services(
        request: Request,
):
    table_name = Item.__name__
    columns = list(ItemSchema.model_fields.keys())

    return app_settings.TEMPLATES.TemplateResponse(
        "creating_page.html",
        {
            "request": request,
            "table_name": table_name,
            "columns": columns
        }
    )


async def item_create_services(
        schema: ItemSchema,
        async_session_maker: async_sessionmaker
):
    """" Создать item. """
    try:
        async with async_session_maker() as session:
            await ItemQueryset.create(
                schema=schema,
                session=session
            )
    except IntegrityError as e:
        error_detail = e.orig.args[0].split('\n')[1]
        raise HTTPException(status_code=422, detail=error_detail)

    return RedirectResponse('/item/instances', status_code=302)


async def item_update_page_services(
        request: Request,
        instance_id: int,
        async_session_maker: async_sessionmaker
):
    """" Страница формы для редактирования текущего item."""

    async with async_session_maker() as session:
        table_name = Item.__name__
        columns = list(ItemSchema.model_fields.keys())
        curr_item = await ItemQueryset.get_by_id(instance_id, session)

    return app_settings.TEMPLATES.TemplateResponse(
        "update_page.html",
        {
            "request": request,
            'table_name': table_name,
            'columns': columns,
            'record': curr_item
        }
    )


async def item_update_services(
        instance_id: int,
        schema: ItemSchema,
        async_session_maker: async_sessionmaker
):
    """" POST-запрос на редактирование записи. """
    try:
        async with async_session_maker() as session:
            await ItemQueryset.update(
                instance_id=instance_id,
                schema=schema,
                session=session
            )
    except IntegrityError as e:
        error_detail = e.orig.args[0].split('\n')[1]
        raise HTTPException(status_code=422, detail=error_detail)

    return RedirectResponse('/item/instances', status_code=302)


async def item_delete_services(
        instance_id: int,
        async_session_maker: async_sessionmaker,
):
    """" Удаление записи. """

    async with async_session_maker() as session:
        await ItemQueryset.delete(
            instance_id=instance_id,
            session=session
        )

    return RedirectResponse('/item/instances', status_code=302)
