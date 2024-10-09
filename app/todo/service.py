

from typing import Annotated
from fastapi import Depends
from app.core.service import BaseService
from app.core.transaction_manager import TManagerDep
from app.todo.models import Todo
from app.users.manager import UserManager, get_user_manager

class TodoService(BaseService):
    ...
    


def get_todo_service(
    transaction_manager: TManagerDep,
    user_manager: UserManager = Depends(get_user_manager),
) -> TodoService:
    return TodoService(Todo, transaction_manager, user_manager)


TodoServiceDep = Annotated[TodoService, Depends(get_todo_service)]