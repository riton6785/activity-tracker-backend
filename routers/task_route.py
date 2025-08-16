from fastapi import APIRouter, Depends, HTTPException

from models import TodoUsers, Projects
from crud import create_task
from sqlalchemy.orm import Session
from dependency import get_db, get_current_user
import schemas

router = APIRouter()

@router.post("/create/task", response_model=schemas.TaskCreateOut)
def create_task_route(task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: TodoUsers = Depends(get_current_user)):
    project_id = db.query(Projects).filter_by(id=task.project_id).first()
    if project_id:
        return create_task(task, db, current_user.id)
    else:
        raise HTTPException(status_code=401, detail="Project id does not found")
