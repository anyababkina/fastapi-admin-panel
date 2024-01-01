import os
from pathlib import Path
from dotenv import load_dotenv
from starlette.templating import Jinja2Templates
from pydantic_settings import BaseSettings

load_dotenv()


class EnvSettings(BaseSettings):
    DB_HOST: str = os.environ.get("DB_HOST")
    DB_PORT: str = os.environ.get("DB_PORT")
    DB_NAME: str = os.environ.get("DB_NAME")
    DB_USER: str = os.environ.get("DB_USER")
    DB_PASS: str = os.environ.get("DB_PASS")


class TestSettings(BaseSettings):
    TEST_POSTGRES_IMAGE: str = "postgres:14"
    TEST_POSTGRES_USER: str = "postgres"
    TEST_POSTGRES_PASSWORD: str = "test_password"
    TEST_POSTGRES_DATABASE: str = "test_database"
    TEST_POSTGRES_CONTAINER_PORT: int = 5432


class AppSettings(BaseSettings):
    ALLOWED_URL: list
    TEMPLATES: Jinja2Templates


BASE_DIR = Path(__file__).resolve().parent

env_settings = EnvSettings()
test_settings = TestSettings()
app_settings = AppSettings(
    ALLOWED_URL=['/login', '/registration', '/docs'],
    TEMPLATES=Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))
)





