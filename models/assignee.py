from sqlalchemy import Table, Column, Integer, ForeignKey
from database import Base

task_assignees = Table(
    'task_assignees',
    Base.metadata,
    Column('task_id', Integer, ForeignKey('project_task.id', ondelete='CASCADE'), primary_key=True),
    Column('user_id', Integer, ForeignKey('todo_users.id', ondelete='CASCADE'), primary_key=True),
)
