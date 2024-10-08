from abc import ABC, abstractmethod
from typing import Type

from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.future import select


class AbstractRepository(ABC):
    @abstractmethod
    async def find_one_or_none(self, **filter_by): ...

    @abstractmethod
    async def find_all(self, **filter_by): ...

    @abstractmethod
    async def insert_data(self, **data): ...

    @abstractmethod
    async def update_fields_by_id(self, entity_id, **data): ...

    @abstractmethod
    async def delete(self, **filter_by): ...
    
    
class SQLAlchemyRepository(AbstractRepository):
    model: Type[DeclarativeMeta] = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_one_or_none(self, **filter_by):
        statement = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def find_all(self, **filter_by):
        statement = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def insert_data(self, **data):
        entity = self.model(**data)
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def update_fields_by_id(self, entity_id, **data):
        statement = update(self.model).where(self.model.id == entity_id).values(**data).execution_options(synchronize_session="fetch")
        result = await self.session.execute(statement)
        await self.session.commit()
        return result.rowcount

    async def delete(self, **filter_by):
        statement = delete(self.model).filter_by(**filter_by).execution_options(synchronize_session="fetch")
        result = await self.session.execute(statement)
        await self.session.commit()
        return result.rowcount
    