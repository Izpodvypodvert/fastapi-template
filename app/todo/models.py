from sqlalchemy import UUID, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.core.models import Base


class Todo(Base):
   __tablename__ = "todo"
   
   id = Column(Integer, primary_key=True, index=True)
   title = Column(String, nullable=False)
   description = Column(String, nullable=True)
   user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
   user = relationship("User", back_populates="todo")