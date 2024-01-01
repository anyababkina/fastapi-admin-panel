import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.models import User


# Перенаправление на страницу со входом при попытке обратиться к страницам, доступным только авторизованным пользователям
@pytest.mark.parametrize('url', ['/user/instances', '/user/instances/1', '/user/instance', '/user/1', '/user/1/delete'])
async def test_redirect_if_user_not_logged(ac, url):
    response = await ac.get(url, follow_redirects=True)
    assert response.status_code == 200
    assert response.url.path == '/login'


# Установка полей, которые нужно отображать в таблице
async def test_update_cookie(ac, get_logged_user):
    response = await ac.post(
        '/user/instances',
        data={'checkbox': ['username']}
    )

    cookie = response.cookies.get('cselected_user')
    assert cookie == "username"


# Создание нового user
async def test_create_user(ac, get_logged_user, prepare_db_and_session_maker: async_sessionmaker):
    response = await ac.post(
        '/user/instance',
        data={"email":'test@test.com', "username":'test', "password": '12345678'},
        follow_redirects=True
    )

    assert response.status_code == 200
    assert response.url.path == '/user/instances'

    async with prepare_db_and_session_maker() as session:
        result = await session.execute(select(User).where(User.email == 'test@test.com'))

        assert result.unique().scalar_one() is not None


# Изменение user
async def test_update_user(ac, get_logged_user, prepare_db_and_session_maker: async_sessionmaker):
    response = await ac.post(
        '/user/1',
        data={"email":'test@test.com', "username":'user1', "password": '12345678'},
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert response.url.path == '/user/instances'

    async with prepare_db_and_session_maker() as session:
        updated_user = await session.get(User, 1)

    assert updated_user.email == 'test@test.com'


# Удаление user
async def test_delete_user(ac, get_logged_user, prepare_db_and_session_maker: async_sessionmaker):
    response = await ac.get(
        '/user/1/delete',
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert response.url.path == '/user/instances'

    async with prepare_db_and_session_maker() as session:
        deleted_post = await session.get(User, 1)

    assert deleted_post is None

