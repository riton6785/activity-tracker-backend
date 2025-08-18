import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL")

def send_invite_email(to_email: str, project, token: str):
    subject = f"Invitation to collaborate on '{project.name}'"
    inviteUrl = f"http://localhost:3000/invite?token={token}"

    body = f"""
    <html>
      <body>
        <p>Hello,</p>

        <p>You've been invited to collaborate on the project: <b>{project.name}</b></p>

        <p>Description: {project.description}</p>

        <p>
            <a href="{inviteUrl}" style="background:#4CAF50;color:white;padding:10px 15px;text-decoration:none;border-radius:5px;">View Invitation</a>
        </p>

        <p>If you didn't expect this, you can ignore this email.</p>

        <p>— Focus Pulse</p>
      </body>
    </html>
    """

    message = MIMEMultipart("alternative")
    message["From"] = formataddr(("Focus Pulse", FROM_EMAIL))
    message["To"] = to_email
    message["Subject"] = subject

    # Use HTML instead of plain
    message.attach(MIMEText(body, "html"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(FROM_EMAIL, to_email, message.as_string())

