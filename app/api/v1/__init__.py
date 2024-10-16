from app.api.v1.routers.oauth import router as oauth_router
from app.api.v1.routers.user_router import router as user_router
from app.api.v1.routers.todo import todo_router


routers_v1 = [
    oauth_router,
    user_router,
    todo_router
]