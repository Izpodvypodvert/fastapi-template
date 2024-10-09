from abc import ABC, abstractmethod
from typing import Generic, Optional, Type, TypeVar, TypedDict

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
    def __init__(self, model: Type[DeclarativeMeta], session: AsyncSession):
        """
        Initializes the repository with a specific SQLAlchemy model and session.

        Args:
            model (Type[DeclarativeMeta]): The SQLAlchemy model class to use for queries.
            session (AsyncSession): The SQLAlchemy asynchronous session for database interactions.
        """
        if not isinstance(model, DeclarativeMeta):
            raise TypeError("model must be a SQLAlchemy declarative model.")
        self.model = model
        self.session = session

    async def find_one_or_none(self, **filter_by):
        statement = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def find_all(self, **filter_by):
        statement = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def insert_data(self, **data: dict):
        entity = self.model(**data)
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def update_fields_by_id(self, entity_id, **data):
        statement = (
        update(self.model)
        .where(getattr(self.model, "id") == entity_id)
        .values(**data)
        .execution_options(synchronize_session="fetch")
    )
        result = await self.session.execute(statement)
        await self.session.commit()
        return result.rowcount

    async def delete(self, **filter_by):
        statement = delete(self.model).filter_by(**filter_by).execution_options(synchronize_session="fetch")
        result = await self.session.execute(statement)
        await self.session.commit()
        return result.rowcount
    