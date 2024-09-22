from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID


Base: DeclarativeMeta  = declarative_base()


class User(SQLAlchemyBaseUserTableUUID, Base):
    username = Column(String, unique=True, nullable=False)

