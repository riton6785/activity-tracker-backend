from fastapi import APIRouter, Depends, HTTPException

from models import TodoUsers, Projects, Tasks
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

@router.get("/task/details/{task_id}")
def get_task_form_details(task_id: int, db: Session = Depends(get_db), current_user: TodoUsers = Depends(get_current_user)):
    task = db.query(Tasks).filter(Tasks.id == task_id).first()
    if task:
        return {
            "project": task.project.name,
            "name": task.name,
            "due_date": task.due_date.strftime("%Y-%m-%d"),
            "created_by": task.owner.name,
            "description": task.description,
            "completed": task.completed,
            "collaborators": [
                    {
                        "id": collaborator.id,
                        "name": collaborator.name,
                    }
                    for collaborator in task.project.collaborators
                ],
                "assignees": [
                    {
                        "id": assignee.id,
                        "name": assignee.name
                    }
                    for assignee in task.assignees
                ]
        }


@router.put("/task/update/{task_id}")
def update_task_details(update_data: schemas.TaskUpdate, db: Session = Depends(get_db), current_user: TodoUsers = Depends(get_current_user)):
    task = db.query(Tasks).filter(Tasks.id == update_data.id).first()
    collaborator_ids = [collaborator.id for collaborator in task.project.collaborators]
    if task and (current_user.id in collaborator_ids or current_user.id == task.user_id):
        task.description = update_data.description
        task.name = update_data.name
        task.due_date = update_data.due_date
        assignee_ids = update_data.assignee_id
        users = db.query(TodoUsers).filter(TodoUsers.id.in_(assignee_ids)).all()
        task.assignees = users
        db.commit()
        db.refresh(task)
        return{"details": "Task updated successfully"}
    
@router.put("/task/markdone/{task_id}")
def mark_done(task_id: int, db: Session = Depends(get_db), current_user: TodoUsers = Depends(get_current_user)):
    breakpoint()
    task = db.query(Tasks).filter(Tasks.id == task_id).first()
    task.completed = True
    db.commit()
    db.refresh(task)
    return{"details": "Marked Done"}
