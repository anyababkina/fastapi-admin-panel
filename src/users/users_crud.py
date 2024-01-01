from fastapi import HTTPException
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth_handler import auth_handler
from src.models import User
from src.users.users_schemas import UserSchema


class UserQueryset:
    model = User

    @classmethod
    async def create(cls, schema: UserSchema, session: AsyncSession) -> User:
        str_password = schema.password.get_secret_value()
        hashed_password = auth_handler.get_password_hash(str_password)

        instance = cls.model(username=schema.username, email=schema.email, password=hashed_password)
        session.add(instance)
        await session.commit()

        return instance

    @classmethod
    async def get_by_id(cls, instance_id: int, session: AsyncSession, selected: list = None) -> User:
        if selected is None:
            instance = await session.get(cls.model, instance_id)
        else:
            query = select(*[getattr(cls.model, c) for c in selected]).where(cls.model.id == instance_id)
            result = await session.execute(query)
            instance = result.fetchone()
        if not instance:
            raise HTTPException(status_code=404, detail="Item obj not found")
        return instance

    @classmethod
    async def get_multiple(cls, session: AsyncSession, selected: list):

        query = select(*[getattr(cls.model, c) for c in selected]).order_by(desc(cls.model.id))
        result = await session.execute(query)

        return result.fetchall()

    @classmethod
    async def update(cls, instance_id: int, schema: UserSchema, session: AsyncSession) -> User:

        str_password = schema.password.get_secret_value()
        hashed_password = auth_handler.get_password_hash(str_password)
        instance = await cls.get_by_id(instance_id, session)

        data = {'username': schema.username, 'email': schema.email, 'password': hashed_password}

        for key, value in data.items():
            setattr(instance, key, value)

        session.add(instance)
        await session.commit()

        return instance

    @classmethod
    async def delete(cls, instance_id: int, session: AsyncSession) -> None:
        instance = await cls.get_by_id(instance_id, session)
        await session.delete(instance)
        await session.commit()

        return None

    @classmethod
    async def get_columns(cls) -> list[str]:
        try:
            field_names = [column.name for column in cls.model.__table__.columns]
        except Exception as e:
            print(e)
            field_names = []
        return field_names
