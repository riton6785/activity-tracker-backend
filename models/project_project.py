from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
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
