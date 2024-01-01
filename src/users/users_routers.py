from typing import Annotated

from fastapi import APIRouter, Request, Depends, Cookie, Form
from starlette.responses import HTMLResponse

from dependency import SessionMakerDep
from src.users.users_schemas import UserSchema
from src.users.users_services import user_table_view_services, user_instance_view_services, user_create_page_services, \
    user_create_services, user_update_page_services, user_update_services, user_delete_services, \
    user_update_cookie_services

users_router = APIRouter(prefix='', tags=['users'])


@users_router.get('/user/instances', response_class=HTMLResponse)
async def user_table_view(
        request: Request,
        async_session_maker: SessionMakerDep,
        cselected_user: str = Cookie(None)
):
    response = await user_table_view_services(
        request=request,
        async_session_maker=async_session_maker,
        cselected_user=cselected_user
    )

    return response


@users_router.post("/user/instances")
async def user_update_cookie(checkbox: Annotated[list, Form(...)]):

    response = await user_update_cookie_services(
        checkbox=checkbox
    )

    return response


@users_router.get('/user/instances/{instance_id}', response_class=HTMLResponse)
async def user_instance_view(
        request: Request,
        instance_id: int,
        async_session_maker: SessionMakerDep,
        cselected_user: str = Cookie(None)
):
    response = await user_instance_view_services(
        request=request,
        instance_id=instance_id,
        async_session_maker=async_session_maker,
        cselected_user=cselected_user
    )

    return response


@users_router.get('/user/instance', response_class=HTMLResponse)
async def user_create_page(request: Request):
    response = await user_create_page_services(
        request=request
    )

    return response


@users_router.post('/user/instance', status_code=201, response_class=HTMLResponse)
async def user_create(
        async_session_maker: SessionMakerDep,
        schema: Annotated[UserSchema, Depends(UserSchema.as_form)],
):
    response = await user_create_services(
        schema=schema,
        async_session_maker=async_session_maker
    )

    return response


@users_router.get('/user/{instance_id}/', response_class=HTMLResponse, status_code=200)
async def user_update_page(
        request: Request,
        instance_id: int,
        async_session_maker: SessionMakerDep,
):
    response = await user_update_page_services(
        request=request,
        instance_id=instance_id,
        async_session_maker=async_session_maker
    )

    return response


@users_router.post('/user/{instance_id}/', status_code=200, response_class=HTMLResponse)
async def user_update(
        instance_id: int,
        async_session_maker: SessionMakerDep,
        schema: Annotated[UserSchema, Depends(UserSchema.as_form)],
):
    response = await user_update_services(
        instance_id=instance_id,
        schema=schema,
        async_session_maker=async_session_maker
    )

    return response


@users_router.get('/user/{instance_id}/delete', status_code=200, response_class=HTMLResponse)
async def user_delete(
        instance_id: int,
        async_session_maker: SessionMakerDep,
):
    response = await user_delete_services(
        instance_id=instance_id,
        async_session_maker=async_session_maker
    )

    return response