import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.models import Item


# Перенаправление на страницу со входом при попытке обратиться к страницам, доступным только авторизованным пользователям
@pytest.mark.parametrize('url', ['/item/instances', '/item/instances/1', '/item/instance', '/item/1', '/item/1/delete'])
async def test_redirect_if_user_not_logged(ac, url):
    response = await ac.get(url, follow_redirects=True)
    assert response.status_code == 200
    assert response.url.path == '/login'


# Установка полей, которые нужно отображать в таблице
async def test_update_cookie(ac, get_logged_user):
    response = await ac.post(
        '/item/instances',
        data={'checkbox': 'name'}
    )

    cookie = response.cookies.get('cselected_item')
    assert cookie == 'name'

# Создание нового item
async def test_create_item(ac, get_logged_user, prepare_db_and_session_maker: async_sessionmaker):
    response = await ac.post(
        '/item/instance',
        data={'name': 'test', 'description': 'test', 'user_id': 1},
        follow_redirects=True
    )

    assert response.status_code == 200
    assert response.url.path == '/item/instances'

    async with prepare_db_and_session_maker() as session:
        result = await session.execute(select(Item).where(Item.name == 'test'))

        assert result.unique().scalar_one() is not None


# Изменение item
async def test_update_item(ac, get_logged_user, prepare_db_and_session_maker: async_sessionmaker):
    response = await ac.post(
        '/item/1',
        data={'name': 'Update', 'description': 'Update', 'user_id': 1},
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert response.url.path == '/item/instances'

    async with prepare_db_and_session_maker() as session:
        updated_item = await session.get(Item, 1)

    assert updated_item.description == 'Update'


# Удаление item
async def test_delete_post(ac, get_logged_user, prepare_db_and_session_maker: async_sessionmaker):
    response = await ac.get(
        '/item/1/delete',
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert response.url.path == '/item/instances'

    async with prepare_db_and_session_maker() as session:
        deleted_item = await session.get(Item, 1)

    assert deleted_item is None


