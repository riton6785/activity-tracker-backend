from sqlalchemy.orm import Session
from models import TodoUsers, Projects
import schemas

def create_project(project: schemas.ProjectCreate, db: Session, current_user: TodoUsers):
    db_project = Projects(**project.dict(), user_id = current_user.id)
    db.add(db_project)
    db_project.collaborators.append(current_user) # Creator will be always a collaborator to his project.
    db.commit()
    db.refresh(db_project)
    return db_project
