from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base

class Todo(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True)
    task = Column(String, nullable=False) # This field is name filed need to rename in future to avoid confusion.
    completed = Column(Boolean, default=False)
    summary = Column(String, default="No summary provided", nullable=True)
    due_date = Column(Date, nullable=False)
    finish_note = Column(String)

    user_id = Column(Integer, ForeignKey('todo_users.id', ondelete='CASCADE'))
    owner = relationship('TodoUsers', back_populates='todos')

    task_id = Column(Integer, ForeignKey('project_task.id', ondelete='CASCADE'), nullable=True)
    linked_task = relationship("Tasks", back_populates='activities')
