from sqlalchemy.orm import Session
from models import TodoUsers, Projects
import schemas

def create_project(project: schemas.ProjectCreate, db: Session, current_user_id: int):
    db_project = Projects(**project.dict(), user_id = current_user_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project
