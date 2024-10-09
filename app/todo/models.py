from sqlalchemy import Column, Integer, String
from app.core.models import Base


class Todo(Base):
   __tablename__ = "todos"
   
   id = Column(Integer, primary_key=True, index=True)
   title = Column(String, nullable=False)
   description = Column(String, nullable=True)