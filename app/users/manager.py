from pydantic import UUID4
import smtplib
from email.mime.text import MIMEText

from fastapi import Depends, HTTPException
from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users.jwt import generate_jwt
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from app.core.db import get_async_session, AsyncSession
from app.core.logger import logger
from app.users.models import User
from app.core.config import settings



async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session=session, user_table=User)


class UserManager(UUIDIDMixin, BaseUserManager[User, UUID4]):
    reset_password_token_secret = settings.secret
    verification_token_secret = settings.secret

    async def on_after_register(self, user: User, request: None = None):
        logger.info(f"User {user.email} has registered.")
        await self._send_verification_email(user)

    async def on_after_forgot_password(self, user: User, token: str, request: None = None):
        await self._send_reset_password_email(user.email, token)

    async def on_after_request_verify(self, user: User, request: None = None):
        logger.info(f"Verification requested for user {user.email}.")
        await self._send_verification_email(user)
        
    async def _handle_smtp_error(self, e: Exception, message: str):
        logger.error(message, exc_info=e)
        raise HTTPException(status_code=500, detail="Ошибка при отправке письма")
               
    async def _send_email(self, subject: str, email: str, message: str):
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = settings.email_address
        msg['To'] = email

        try:
            with smtplib.SMTP(settings.smtp_address, settings.smtp_port) as server:
                server.starttls()
                server.login(settings.email_address, settings.email_password)
                server.send_message(msg)
        except OSError as e:
            error_message = f"Ошибка сети при отправке письма: {e}" if e.errno == 101 else f"Ошибка ОС при отправке письма: {e}"
            await self._handle_smtp_error(e, error_message)
        except (smtplib.SMTPConnectError, smtplib.SMTPAuthenticationError, smtplib.SMTPException) as e:
            await self._handle_smtp_error(e, f"Ошибка SMTP: {e}")

                    
    async def _send_reset_password_email(self, email: str, token: str):
        reset_url = f"{settings.reset_password_url}={token}"
        message = f"Для восстановления пароля перейдите по следующей ссылке: {reset_url}"
        await self._send_email('Восстановление пароля', email, message)

    async def _send_verification_email(self, user: User):
        if user.is_verified:
            raise HTTPException(status_code=400, detail="Почта пользователя уже подтверждена!")
        token = await self._generate_token(user)
        verification_url = f"{settings.verification_url}={token}"
        message = f"Для верификации email перейдите по следующей ссылке: {verification_url}"
        await self._send_email('Верификация email', user.email, message)

    async def _generate_token(self, user: User) -> str:
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "aud": self.verification_token_audience,
        }
        token = generate_jwt(
            token_data,
            self.verification_token_secret,
            self.verification_token_lifetime_seconds,
            )
        return token

async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
    