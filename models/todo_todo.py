from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base
from datetime import date, timedelta

class Todo(Base):
    __tablename__ = "todos"

    def default_date(self):
        return date.today + timedelta(days=30)
    
    id = Column(Integer, primary_key=True)
    task = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
    summary = Column(String, default="No summary provided", nullable=True)
    due_date = Column(Date, default=default_date, nullable=True)
    finish_note = Column(String)

    user_id = Column(Integer, ForeignKey('todo_users.id', ondelete='CASCADE'))
    owner = relationship('TodoUsers', back_populates='todos')

