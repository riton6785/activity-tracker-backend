from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .collaborators import project_collaborators
from database import Base

class TodoUsers(Base):
    __tablename__ = "todo_users"

    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    password = Column(String, nullable = False)
    email = Column(String, nullable = False)
    purpose = Column(String, nullable = False, default="My purpose is secret")
    mobile_no = Column(String, nullable = False, default="9898989898")

    todos = relationship('Todo', back_populates='owner', cascade="all, delete", passive_deletes=True)
    projects = relationship('Projects', back_populates='owner', cascade="all, delete", passive_deletes=True)
    tasks = relationship('Tasks', back_populates='owner', foreign_keys='Tasks.user_id', cascade="all, delete", passive_deletes=True) # This relationship holds the tasks which are created by the user.
    assigned_tasks = relationship('Tasks', back_populates='assignee', foreign_keys='Tasks.assignee_id', cascade="all, delete", passive_deletes=True) # This relation holds the tasks where the user is assigned to the task.

    # Project collaborators flow
    collaborating_projects = relationship(
        "Projects",
        secondary=project_collaborators,
        back_populates="collaborators",
    )
