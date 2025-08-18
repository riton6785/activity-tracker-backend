from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from .collaborators import project_collaborators
from database import Base

class Projects(Base):
    __tablename__ = "project_project"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey('todo_users.id', ondelete='CASCADE'))
    owner = relationship('TodoUsers', back_populates='projects')
    due_date = Column(Date, nullable=False)
    completed = Column(Boolean, default=False)

    tasks = relationship('Tasks', back_populates='project', cascade="all, delete", passive_deletes=True)

    # Inviting a collaborators flow.
    collaborators = relationship(
        "TodoUsers",
        secondary=project_collaborators,
        back_populates="collaborating_projects",
    )

    invites = relationship(
        "ProjectInvite",
        back_populates="project",
        cascade="all, delete-orphan",
    )
