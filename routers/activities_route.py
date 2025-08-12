from fastapi import APIRouter, Depends, HTTPException

from models import TodoUsers
from crud import get_completed_activities, create_todo, get_overdue_todos, get_todos, get_todo_by_id, delete_todo, toggle_todo_completed, update_activity
from sqlalchemy.orm import Session
from dependency import get_db, get_current_user
import schemas


router = APIRouter()

@router.post("/activities/", response_model=schemas.TodoOut)
def create_todo_route(todo: schemas.TodoCreate, db: Session = Depends(get_db), current_user: TodoUsers = Depends(get_current_user)):
    return create_todo(db, todo, current_user.id)

@router.get("/activities/", response_model=list[schemas.TodoOut], )
def read_todos(db: Session = Depends(get_db), current_user: TodoUsers = Depends(get_current_user)):
    return get_todos(db, current_user)

@router.get("/overdue/activities", response_model=list[schemas.TodoOut])
def read_overdue_activities(db: Session = Depends(get_db), current_user: TodoUsers = Depends(get_current_user)):
    return get_overdue_todos(db, current_user)

@router.get("/completed/activities", response_model=list[schemas.TodoOut])
def read_completed_activities(db: Session = Depends(get_db), current_user: TodoUsers = Depends(get_current_user)):
    return get_completed_activities(db, current_user)

@router.get("/activity/{id}", response_model=schemas.TodoOut)
def read_todo(id: int, db: Session = Depends(get_db)):
    todo = get_todo_by_id(db, id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.delete("/activity/{id}")
def delete_todo_route(
    id: int,
    db: Session = Depends(get_db),
    current_user: TodoUsers = Depends(get_current_user)
):
    success = delete_todo(db, id, current_user)

    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Deleted successfully"}

@router.put("/activity/toggle", response_model=schemas.TodoOut)
def toggle_todo_route(
    toggle_data: schemas.ToggleNote,
    db: Session = Depends(get_db),
    current_user: TodoUsers = Depends(get_current_user)
):
    updated_todo = toggle_todo_completed(db, current_user, toggle_data)
    if not updated_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated_todo

@router.put("/edit/activity", response_model=schemas.TodoOut)
def edit_Activities(
    activity: schemas.EditActivities,
    db: Session = Depends(get_db),
    current_user: TodoUsers = Depends(get_current_user)
):
    updated_activity = update_activity(db, current_user, activity)
    if not updated_activity:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated_activity