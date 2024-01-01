from typing import Annotated

from fastapi import APIRouter, Request, Depends, Form, Cookie
from starlette.responses import HTMLResponse

from dependency import SessionMakerDep
from src.items.items_schemas import ItemSchema
from src.items.items_services import item_table_view_services, item_instance_view_services, item_create_page_services, \
    item_create_services, item_update_page_services, item_update_services, item_delete_services, \
    item_update_cookie_services

items_router = APIRouter(prefix='', tags=['items'])


@items_router.get('/item/instances', response_class=HTMLResponse)
async def item_table_view(
        request: Request,
        async_session_maker: SessionMakerDep,
        cselected_item: str = Cookie(None)
):
    response = await item_table_view_services(
        request=request,
        async_session_maker=async_session_maker,
        cselected_item=cselected_item
    )

    return response


@items_router.post("/item/instances")
async def item_update_cookie(checkbox: Annotated[list, Form(...)]):

    response = await item_update_cookie_services(
        checkbox=checkbox
    )

    return response


@items_router.get('/item/instances/{instance_id}', response_class=HTMLResponse)
async def item_instance_view(
        request: Request,
        instance_id: int,
        async_session_maker: SessionMakerDep,
        cselected_item: str = Cookie(None)
):
    response = await item_instance_view_services(
        request=request,
        instance_id=instance_id,
        async_session_maker=async_session_maker,
        cselected_item=cselected_item
    )

    return response


@items_router.get('/item/instance', response_class=HTMLResponse)
async def item_create_page(request: Request):
    response = await item_create_page_services(
        request=request
    )

    return response


@items_router.post('/item/instance', status_code=201, response_class=HTMLResponse)
async def item_create(
        async_session_maker: SessionMakerDep,
        schema: Annotated[ItemSchema, Depends(ItemSchema.as_form)],
):
    response = await item_create_services(
        schema=schema,
        async_session_maker=async_session_maker
    )

    return response


@items_router.get('/item/{instance_id}', response_class=HTMLResponse, status_code=200)
async def item_update_page(
        request: Request,
        instance_id: int,
        async_session_maker: SessionMakerDep,
):
    response = await item_update_page_services(
        request=request,
        instance_id=instance_id,
        async_session_maker=async_session_maker
    )

    return response


@items_router.post('/item/{instance_id}', status_code=200, response_class=HTMLResponse)
async def item_update(
        instance_id: int,
        async_session_maker: SessionMakerDep,
        schema: Annotated[ItemSchema, Depends(ItemSchema.as_form)],
):
    response = await item_update_services(
        instance_id=instance_id,
        schema=schema,
        async_session_maker=async_session_maker
    )

    return response


@items_router.get('/item/{instance_id}/delete', status_code=200, response_class=HTMLResponse)
async def item_delete(
        instance_id: int,
        async_session_maker: SessionMakerDep,
):
    response = await item_delete_services(
        instance_id=instance_id,
        async_session_maker=async_session_maker
    )

    return response
