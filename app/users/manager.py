from pydantic import UUID4
from fastapi import Depends
from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from app.core.db import get_async_session, AsyncSession
from app.users.models import User
from app.core.config import settings



async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session=session, user_table=User)


class UserManager(UUIDIDMixin, BaseUserManager[User, UUID4]):
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