from app.core.repository import SQLAlchemyRepository
from app.todo.models import Todo


class TodoRepository(SQLAlchemyRepository):
    ...