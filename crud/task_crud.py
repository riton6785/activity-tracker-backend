from sqlalchemy.orm import Session
from models import Tasks
import schemas

def create_task(task: schemas.TaskCreate, db: Session, current_user_id: int):
    db_task = Tasks(**task.dict(), user_id = current_user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task