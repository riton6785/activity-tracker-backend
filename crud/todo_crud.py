from sqlalchemy.orm import Session
from models import Todo, TodoUsers
import schemas

def get_todos(db: Session, current_user: TodoUsers):
    return db.query(Todo).filter(Todo.user_id == current_user.id).all()

def get_todo_by_id(db: Session, todo_id: int):
    return db.query(Todo).filter(Todo.id == todo_id).first()

def create_todo(db: Session, todo: schemas.TodoCreate, user_id: int):
    db_todo = Todo(**todo.dict(), user_id = user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, todo_id: int, current_user: TodoUsers):
    todo = get_todo_by_id(db, todo_id)
    if todo and todo.user_id == current_user.id:
        db.delete(todo)
        db.commit()
        return True
    return False

def toggle_todo_completed(db: Session, todo_id: int, current_user: TodoUsers):
    todo = get_todo_by_id(db, todo_id)
    if todo and todo.user_id == current_user.id:
        todo.completed = not todo.completed
        db.commit()
        db.refresh(todo)
        return todo
    return None