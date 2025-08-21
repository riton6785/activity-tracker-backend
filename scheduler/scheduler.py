# scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from database import SessionLocal
from models import Todo, TodoUsers, Tasks, Projects
from scheduler.email import send_reminder_email

def get_due_activities(session: Session):
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    return session.query(Todo).filter(
        Todo.due_date.in_([today, tomorrow]),
        Todo.completed == False
    ).all()

def get_due_task(session: Session):
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    return session.query(Tasks).filter(
        Tasks.due_date.in_([today, tomorrow]),
        Tasks.completed == False
    ).all()

def get_due_project(session: Session):
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    return session.query(Projects).filter(
        Projects.due_date.in_([today, tomorrow]),
        Projects.completed == False
    ).all()

def job():
    db = SessionLocal()
    activities = get_due_activities(db)
    projects = get_due_project(db)
    tasks = get_due_task(db)
    
    for activity in activities:
        user = db.query(TodoUsers).filter(TodoUsers.id == activity.user_id).first()
        if user and user.email:
            send_reminder_email(user.email, activity, "Activities")
    
    for project in projects:
        for collaborator in project.collaborators:
            send_reminder_email(collaborator.email, project, "Project")
    
    for task in tasks:
        for assignee in task.assignees:
            send_reminder_email(assignee.email, task, "Task")
    
    db.close()

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(job, 'interval', hours=8)
    scheduler.start()
