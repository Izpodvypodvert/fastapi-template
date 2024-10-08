from typing import TYPE_CHECKING, Type

from app.core.repository import AbstractRepository
from app.core.transaction_manager import ITransactionManager

from app.core.exceptions import IncorrectIdException, MissingRepositoryError


if TYPE_CHECKING:
    from app.users.manager import UserManager


class BaseService[T]:
    def __init__(
        self,
        entity_type: Type[T],
        transaction_manager: ITransactionManager,
        user_manager: "UserManager",
    ):
        self.entity_type = entity_type
        self.transaction_manager = transaction_manager
        self._repository: AbstractRepository = None
        self.user_manager = user_manager

    @property
    def repository(self):
        if self._repository is None:
            try:
                self._repository = getattr(
                    self.transaction_manager, self.entity_type.__name__.lower()
                )
            except AttributeError as e:
                raise MissingRepositoryError(self.entity_type.__name__.lower()) from e
        return self._repository

    async def get_all(self) -> list[T] | None:
        async with self.transaction_manager:
            return await self.repository.find_all()

    async def get_by_id(self, entity_id) -> T | None:
        async with self.transaction_manager:
            entity = await self.repository.find_one_or_none(id=entity_id)
            if not entity:
                raise IncorrectIdException(f"Incorrect {self.entity_type.__name__} id")
            return entity

    async def create(self, entity: T) -> T:
        async with self.transaction_manager:
            return await self.repository.insert_data(**entity.model_dump())

    async def delete(self, entity_id: int) -> int:
        async with self.transaction_manager:
            return await self.repository.delete(id=entity_id)

    async def update(self, entity_id, **data) -> int:
        async with self.transaction_manager:
            return await self.repository.update_fields_by_id(entity_id, **data)
