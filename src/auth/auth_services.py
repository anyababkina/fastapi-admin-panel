from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker
from starlette.responses import RedirectResponse

from src.auth.auth_crud import AdminQueryset
from src.auth.auth_handler import auth_handler
from src.auth.auth_schemas import AdminRegistration, AdminLogin


async def registration_services(
        schema: AdminRegistration,
        async_session_maker: async_sessionmaker
):

    """" Создаем админа (регистрируем), перенаправляем сразу на страницу авторизации в случае успеха """

    try:
       async with async_session_maker() as session:
           await AdminQueryset.create(
               schema=schema,
               session=session
           )
       return RedirectResponse('/login', status_code=302)

    except IntegrityError:
        raise HTTPException(status_code=422, detail="Username and/or email is occupied")


async def login_services(
        schema: AdminLogin,
        async_session_maker: async_sessionmaker
):
    """" Аутентификация и авторизация админа, проверяем валидность данных, создаем токен,
    отдаем его в куки для идентификации залогиненного пользователя """

    async with async_session_maker() as session:
        logged_user = await AdminQueryset.get_by_email(
            schema=schema,
            session=session
        )

        token = auth_handler.encode_token(logged_user.id)

    response = RedirectResponse('/', status_code=302)
    response.set_cookie('admin_cookie', token)

    return response


async def logout_services():
    response = RedirectResponse('/', status_code=302)
    response.delete_cookie('admin_cookie')
    response.delete_cookie('cselected_item')
    response.delete_cookie('cselected_user')
    return response


