from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker
from database import async_session_maker


async def get_session_maker() -> async_sessionmaker:
    yield async_session_maker


SessionMakerDep = Annotated[async_sessionmaker, Depends(get_session_maker)]


