from abc import ABC, abstractmethod
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio.session import async_sessionmaker, AsyncSession

from app.core.db import async_session_maker
from app.todo.models import Todo
from app.todo.repository import TodoRepository

class ITransactionManager(ABC):
    """Interface for implementing the UOW pattern
    for working with transactions to the database"""

    @abstractmethod
    def __init__(self): ...

    @abstractmethod
    async def __aenter__(self): ...

    @abstractmethod
    async def __aexit__(self, *args): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...
    

class TransactionManager(ITransactionManager):
    """Implementation of the interface for working with transactions"""

    def __init__(self, session_factory):
        self.session_factory: async_sessionmaker[AsyncSession] = session_factory

    async def __aenter__(self):
        """
        Asynchronous context manager entry point.

        This method initializes a new session and creates repositories for each model.
        Each repository is assigned as an attribute of the `TransactionManager` instance.
        The attribute names should correspond to the name of the model in lower case.

        For example:
        `TodoRepository` should be assigned to `self.todo`:
        self.todo = TodoRepository(self.session)

        This naming convention ensures consistency when accessing repositories during transactions.

        Returns:
            self: The instance of `TransactionManager` with initialized repositories.
        """
        self.session: AsyncSession = self.session_factory()
        self.todo = TodoRepository(Todo, self.session)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if exc is None:
            await self.session.commit()
        else:
            await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()


def get_transaction_manager(session_factory) -> ITransactionManager:
    return TransactionManager(session_factory)


# return a Unit of work instance for working with Session
TManagerDep = Annotated[
    ITransactionManager,
    Depends(lambda: get_transaction_manager(async_session_maker)),
]
