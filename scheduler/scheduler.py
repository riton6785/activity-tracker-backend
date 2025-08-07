# scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from database import SessionLocal
from models import Todo, TodoUsers
from scheduler.email import send_reminder_email

def get_due_tasks(session: Session):
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    return session.query(Todo).filter(
        Todo.due_date.in_([today, tomorrow]),
        Todo.completed == False
    ).all()

def job():
    db = SessionLocal()
    tasks = get_due_tasks(db)
    
    for task in tasks:
        user = db.query(TodoUsers).filter(TodoUsers.id == task.user_id).first()
        if user and user.email:
            send_reminder_email(user.email, task)
    
    db.close()

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(job, 'interval', hours=8)
    scheduler.start()
