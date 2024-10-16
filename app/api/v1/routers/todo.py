from app.core.router import BaseRouterWithUser
from app.todo.service import get_todo_service
from app.todo.schemas import TodoRead, TodoCreate, TodoUpdate
from app.users.auth_config import current_active_user


todo_router = BaseRouterWithUser(
    model=TodoRead,
    model_create=TodoCreate,
    model_update=TodoUpdate,
    service_dependency=get_todo_service,
    prefix="/todos",
    tags=["todos"],
    current_user=current_active_user
).router

