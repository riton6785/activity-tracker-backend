from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from database import Base
from .assignee import task_assignees


class Tasks(Base):
    __tablename__ = 'project_task'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)

    project_id = Column(Integer, ForeignKey('project_project.id', ondelete='CASCADE'))
    project = relationship('Projects', back_populates='tasks')
    user_id = Column(Integer, ForeignKey('todo_users.id', ondelete='CASCADE'))
    owner = relationship('TodoUsers', back_populates='tasks', foreign_keys=[user_id])
    assignees = relationship('TodoUsers', secondary=task_assignees, back_populates='tasks_assigned')
    due_date = Column(Date, nullable=True)
    completed = Column(Boolean, default=False)

    activities = relationship('Todo', back_populates='linked_task', cascade="all, delete", passive_deletes=True)
