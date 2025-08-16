from fastapi import APIRouter, Depends, HTTPException

from models import TodoUsers, Projects, Tasks
from crud import create_project
from sqlalchemy.orm import Session
from dependency import get_db, get_current_user
import schemas

router = APIRouter()

@router.post('/create/project', response_model=schemas.ProjectCreateOut)
def create_project_route(project:schemas.ProjectCreate, db: Session = Depends(get_db), current_user: TodoUsers = Depends(get_current_user)):
    return create_project(project, db, current_user.id)

@router.get("/projects", response_model=list[schemas.ProjectCreateOut])
def readProjects(db: Session = Depends(get_db), current_user: TodoUsers = Depends(get_current_user)):
    return db.query(Projects).filter(Projects.user_id == current_user.id).all()

@router.get("/project/{project_id}/tasks", response_model=list[schemas.TaskCreateOut])
def get_tasks_for_project(project_id: int, db: Session = Depends(get_db)):
    # Check if project exists.
    project = db.query(Projects).filter(Projects.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    tasks = db.query(Tasks).filter(Tasks.project_id == project_id).all()
    return tasks
