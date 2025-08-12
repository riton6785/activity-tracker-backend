from sqlalchemy import Column, Integer, String
from database import Base

class Projects(Base):
    __tablename__ = "project_project"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
