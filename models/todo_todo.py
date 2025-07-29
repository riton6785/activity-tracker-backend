from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    task = Column(String, nullable=False)
    completed = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey('todo_users.id', ondelete='CASCADE'))
    owner = relationship('TodoUsers', back_populates='todos')
