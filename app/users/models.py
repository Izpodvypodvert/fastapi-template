from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseOAuthAccountTableUUID, SQLAlchemyBaseUserTableUUID

from app.core.models import Base


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    """
    Модель OAuthAccount расширяет SQLAlchemyBaseOAuthAccountTableUUID, 
    которая включает поля, необходимые для хранения данных OAuth.
    """


class User(SQLAlchemyBaseUserTableUUID, Base):
    """
    Модель пользователя расширяет SQLAlchemyBaseUserTableUUID для поддержки UUID, 
    а также включает связь с таблицей OAuth аккаунтов.
    """
    username = Column(String, unique=True, nullable=False)
    oauth_accounts = relationship("OAuthAccount", lazy="joined", cascade="all, delete-orphan")
