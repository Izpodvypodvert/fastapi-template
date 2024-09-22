from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import relationship
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from uuid import uuid4

Base: DeclarativeMeta  = declarative_base()


class User(SQLAlchemyBaseUserTableUUID, Base):
    username = Column(String, unique=True, nullable=True)

