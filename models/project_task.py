from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from database import Base


class Tasks(Base):
    __tablename__ = 'project_task'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)

    project_id = Column(Integer, ForeignKey('project_project.id', ondelete='CASCADE'))
    project = relationship('Projects', back_populates='tasks')
    user_id = Column(Integer, ForeignKey('todo_users.id', ondelete='CASCADE'))
    owner = relationship('TodoUsers', back_populates='tasks', foreign_keys=[user_id])
    assignee_id = Column(Integer, ForeignKey('todo_users.id', ondelete='CASCADE'), nullable=True)
    assignee = relationship('TodoUsers', back_populates='assigned_tasks', foreign_keys=[assignee_id])
    due_date = Column(Date, nullable=True)
    completed = Column(Boolean, default=False)
