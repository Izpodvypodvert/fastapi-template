from pydantic import UUID4
from fastapi_users import  FastAPIUsers
from fastapi_users.authentication import (
    BearerTransport,
    AuthenticationBackend,
    JWTStrategy
)
from app.core.config import settings
from app.users.models import User
from app.users.oauth_config import google_oauth_backend
from app.users.manager import get_user_manager


# Настройка транспорта для Cookie
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

# Стратегия JWT
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.secret, lifetime_seconds=3600)

# Настройка бэкенда аутентификации
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, UUID4](
    get_user_manager,
    [auth_backend, google_oauth_backend],
)

current_active_user = fastapi_users.current_user(active=True)