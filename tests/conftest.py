import asyncio
import pytest
from httpx import AsyncClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from testcontainers.core.waiting_utils import wait_for_logs
from testcontainers.core import utils
from testcontainers.postgres import PostgresContainer

from dependency import get_session_maker
from main import app
from settings import test_settings
from src.auth.auth_handler import auth_handler
from src.models import Base, User, Item, Admin


@pytest.fixture(scope="session")
async def postgres_container() -> PostgresContainer:

    """ Тест контейнер """

    postgres = PostgresContainer(
        image=test_settings.TEST_POSTGRES_IMAGE,
        user=test_settings.TEST_POSTGRES_USER,
        password=test_settings.TEST_POSTGRES_PASSWORD,
        dbname=test_settings.TEST_POSTGRES_DATABASE,
        port=test_settings.TEST_POSTGRES_CONTAINER_PORT,
    )
    with postgres:
        postgres.driver = "asyncpg"
        wait_for_logs(
            postgres,
            r"UTC \[1\] LOG:  database system is ready to accept connections",
            10,
        )
        yield postgres


@pytest.fixture(scope="function", autouse=True)
async def prepare_db_and_session_maker(postgres_container: PostgresContainer) -> async_sessionmaker:

    """" Соединение с тест контейнером бд, создание таблиц, создание данных в таблицах для тестов. Получение сессии. """

    if utils.is_windows():
        postgres_container.get_container_host_ip = lambda: "localhost"
    url = postgres_container.get_connection_url()
    engine = create_async_engine(url)

    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)
        await connect.execute(
            insert(User),
            [
                {"email":'user1@example.com', "username":'user1', "password": auth_handler.get_password_hash('12345678')},
                {"email":'user2@example.com', "username":'user2', "password": auth_handler.get_password_hash('12345678')},
            ]
        )
        await connect.execute(
            insert(Item),
            [
                {'user_id': 1, 'name': 'test1', 'description': 'test1'},
                {'user_id': 2, 'name': 'test2', 'description': 'test2'},
            ]
        )
        await connect.execute(
            insert(Admin),
            [
                {"email": 'admin@example.com', "username": 'admin', "password": auth_handler.get_password_hash('12345678')},
            ]
        )

    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

    yield async_session_maker

    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function", autouse=True)
async def override(prepare_db_and_session_maker):
    app.dependency_overrides[get_session_maker] = lambda: prepare_db_and_session_maker

    yield

    app.dependency_overrides.clear()


@pytest.fixture()
async def ac() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='function')
async def get_logged_user(ac):

    """" Получить авторизованного пользователя (для тестов с постами). Выйти после теста. """

    await ac.post(
        '/login',
        data={'email': 'admin@example.com', 'password': '12345678'},
        follow_redirects=False
    )

    yield

    await ac.get(
        '/logout',
        follow_redirects=False
    )



