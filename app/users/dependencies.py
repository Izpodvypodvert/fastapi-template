from pydantic import UUID4
from fastapi import Depends
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from fastapi_users.authentication import (
    CookieTransport,
    AuthenticationBackend,
    JWTStrategy
)
from app.core.db import get_async_session, AsyncSession
from app.core.config import settings
from app.users.models import User


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session=session, user_table=User)


# Настройка транспорта для Cookie
cookie_transport = CookieTransport(cookie_max_age=3600)

# Стратегия JWT
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.secret, lifetime_seconds=3600)

# Настройка бэкенда аутентификации
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

class UserManager(UUIDIDMixin,BaseUserManager[User, UUID4]):
    reset_password_token_secret = settings.secret
    verification_token_secret = settings.secret

    async def on_after_register(self, user: User, request: None = None):
        print(f"User {user.email} has registered.")

    async def on_after_forgot_password(self, user: User, token: str, request: None = None):
        print(f"User {user.email} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(self, user: User, token: str, request: None = None):
        print(f"Verification requested for user {user.email}. Verification token: {token}")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, UUID4](
    get_user_manager,
    [auth_backend],
)

current_active_user = fastapi_users.current_user(active=True)
