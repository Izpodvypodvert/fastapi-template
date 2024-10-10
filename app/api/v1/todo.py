from app.core.router import BaseRouter
from app.todo.service import get_todo_service
from app.todo.schemas import TodoRead, TodoCreate, TodoUpdate


todo_router = BaseRouter(
    model=TodoRead,
    model_create=TodoCreate,
    model_update=TodoUpdate,
    service_dependency=get_todo_service,
    prefix="/todos",
    tags=["todos"],
).router

