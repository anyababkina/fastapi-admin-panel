from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from settings import env_settings

DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{env_settings.DB_USER}:{env_settings.DB_PASS}@{env_settings.DB_HOST}:{env_settings.DB_PORT}/{env_settings.DB_NAME}"
)

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)