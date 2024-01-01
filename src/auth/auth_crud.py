from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth_handler import auth_handler
from src.auth.auth_schemas import AdminRegistration, AdminLogin
from src.models import Admin


class AdminQueryset:
    model = Admin

    @classmethod
    async def create(cls, schema: AdminRegistration, session: AsyncSession) -> Admin:
        str_password = schema.password.get_secret_value()
        hashed_password = auth_handler.get_password_hash(str_password)

        instance = cls.model(username=schema.username, email=schema.email, password=hashed_password)
        session.add(instance)
        await session.commit()

        return instance

    @classmethod
    async def get_by_email(cls, schema: AdminLogin, session: AsyncSession) -> Admin:
        query = select(cls.model).where(cls.model.email == schema.email)
        res = await session.execute(query)
        instance = res.scalars().first()

        if (instance is None) or (not auth_handler.verify_password(schema.password.get_secret_value(), instance.password)):
            raise HTTPException(status_code=401, detail="Invalid email and/or password")

        return instance

    @classmethod
    async def get_by_id(cls, instance_id: int, session: AsyncSession) -> Admin:
        instance = await session.get(cls.model, instance_id)
        if not instance:
            raise HTTPException(status_code=404, detail="Admin not found")
        return instance

    # @classmethod
    # async def get_by_token(cls, token: str, session: AsyncSession) -> Admin:
    #     instance_id = auth_handler.decode_token(token)
    #
    #     instance = await session.get(cls.model, instance_id)
    #     if not instance:
    #         raise HTTPException(status_code=404, detail="Admin obj not found")
    #
    #     return instance




