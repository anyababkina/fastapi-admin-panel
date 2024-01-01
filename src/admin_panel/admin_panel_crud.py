from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession


class Queryset:

    def __init__(self, model):
        self.model = model

    async def count(self, session: AsyncSession) -> int:

        query = select(func.count()).select_from(self.model)
        result = await session.execute(query)

        return result.scalar_one()