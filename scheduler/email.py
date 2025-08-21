# email.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import os
from dotenv import load_dotenv
import re

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL")

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


def send_reminder_email(to_email: str, task, type):
    if not is_valid_email(to_email):
        print(f"Invalid email skipped: {to_email}")
        return  # Skip invalid emails

# THis one is useless need to remove it future because currently activities model have task field where name is stored need to rename that field in future in that case no need for this if condition.
    if type == "Activities":
        subject = f"Reminder: {type} '{task.task}' is due soon!"
        title = task.task
    else:
        subject = f"Reminder: {type} '{task.name}' is due soon!"
        title = task.name

    body = f"""
    Hello,

    This is a reminder that your task:

    Title: {title}
    Due: {task.due_date}

    Please make sure to complete it on time.

    Best regards,
    Activity Tracker
    """

    message = MIMEMultipart()
    message["From"] = formataddr(("Focus Pulse", FROM_EMAIL))
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(FROM_EMAIL, to_email, message.as_string())
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")