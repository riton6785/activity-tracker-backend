from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class TodoUsers(Base):
    __tablename__ = "todo_users"

    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    password = Column(String, nullable = False)
    email = Column(String, nullable = False)

    todos = relationship('Todo', back_populates='owner', cascade="all, delete", passive_deletes=True)
    