# email.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL")

def send_reminder_email(to_email: str, task):
    subject = f"Reminder: Task '{task.task}' is due soon!"
    body = f"""
    Hello,

    This is a reminder that your task:
    
    Title: {task.task}
    Due: {task.due_date}

    Please make sure to complete it on time.

    Best regards,
    Activity Tracker
    """

    message = MIMEMultipart()
    message["From"] = formataddr(("Focus Pulse", FROM_EMAIL))
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(FROM_EMAIL, to_email, message.as_string())
