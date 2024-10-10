

from typing import Annotated, cast
from fastapi import Depends
from app.core.exceptions import IncorrectIdException
from app.core.service import BaseService
from app.core.transaction_manager import TManagerDep
from app.todo.models import Todo
from app.users.manager import UserManager, get_user_manager

class TodoService(BaseService):
    ...
    # async def get_all(self) -> list[T] | None:
    #     async with self.transaction_manager:
    #         return await self.repository.find_all()

    # async def get_by_id(self, entity_id) -> T | None:
    #     async with self.transaction_manager:
    #         entity = await self.repository.find_one_or_none(id=entity_id)
    #         if not entity:
    #             raise IncorrectIdException(f"Incorrect {self.entity_type.__name__} id")
    #         return entity

    # async def create(self, entity: T) -> T:
    #     async with self.transaction_manager:
    #         created_entity = await self.repository.insert_data(**entity.model_dump())
    #         return cast(T, created_entity)

    # async def delete(self, entity_id: int) -> int:
    #     async with self.transaction_manager:
    #         deleted_count = await self.repository.delete(id=entity_id)
    #         return cast(int, deleted_count)

    # async def update(self, entity_id, **data) -> int:
    #     async with self.transaction_manager:
    #         updated_count = await self.repository.update_fields_by_id(entity_id, **data)
    #         return cast(int, updated_count)

    


def get_todo_service(
    transaction_manager: TManagerDep,
    user_manager: UserManager = Depends(get_user_manager),
) -> TodoService:
    return TodoService(Todo, transaction_manager, user_manager)


TodoServiceDep = Annotated[TodoService, Depends(get_todo_service)]