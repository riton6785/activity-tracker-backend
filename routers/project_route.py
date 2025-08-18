from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.security import HTTPAuthorizationCredentials

from models import TodoUsers, Projects, Tasks
from sqlalchemy.orm import Session
from crud import create_project
from models import ProjectInvite, InviteStatus as DBInviteStatus
from dependency import get_db, get_current_user
from utils import send_invite_email, make_invite_token, parse_invite_token
import schemas

from datetime import datetime, timedelta

router = APIRouter()

@router.post('/create/project', response_model=schemas.ProjectCreateOut)
def create_project_route(project:schemas.ProjectCreate, db: Session = Depends(get_db), current_user: TodoUsers = Depends(get_current_user)):
    return create_project(project, db, current_user.id)

@router.get("/projects", response_model=list[schemas.ProjectCreateOut])
def readProjects(db: Session = Depends(get_db), current_user: TodoUsers = Depends(get_current_user)):
    return db.query(Projects).filter(Projects.user_id == current_user.id).all()

@router.get("/project/{project_id}/tasks", response_model=list[schemas.TaskCreateOut])
def get_tasks_for_project(project_id: int, db: Session = Depends(get_db)):
    # Check if project exists.
    project = db.query(Projects).filter(Projects.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    tasks = db.query(Tasks).filter(Tasks.project_id == project_id).all()
    return tasks

def mask_email(e: str) -> str:
    try:
        name, domain = e.split("@")
        return name[0] + "*****@" + domain
    except:
        return "***"

@router.post("/project/{project_id}/invite", response_model=schemas.InviteOut)
def invite_user(
    project_id: int,
    payload: schemas.InviteCreate,
    db: Session = Depends(get_db),
    current_user: TodoUsers = Depends(get_current_user),
):
    project = db.query(Projects).get(project_id)
    if not project:
        raise HTTPException(404, "Project not found")
    if project.user_id != current_user.id:
        raise HTTPException(403, "Only the owner can invite collaborators")

    email = payload.email.lower()
    if email == current_user.email.lower():
        raise HTTPException(400, "You cannot invite yourself")

    # Already a collaborator?
    if any(u.email.lower() == email for u in project.collaborators):
        raise HTTPException(409, "User is already a collaborator")

    # Existing pending invite?
    existing = (
        db.query(ProjectInvite)
        .filter(
            ProjectInvite.project_id == project_id,
            ProjectInvite.invitee_email == email,
            ProjectInvite.status == DBInviteStatus.pending,
        )
        .first()
    )
    if existing:
        raise HTTPException(409, "An invite is already pending for this email")

    invite = ProjectInvite(
        project_id=project_id,
        inviter_id=current_user.id,
        invitee_email=email,
        status=DBInviteStatus.pending,
    )
    db.add(invite)
    db.commit()
    db.refresh(invite)

    token = make_invite_token(invite.id, invite.token_nonce)
    send_invite_email(email, project, token)

    return invite

@router.get("/project/invites/resolve")
def resolve_invite(
    request: Request,
    token: str = Query(...),
    db: Session = Depends(get_db),
):
    parsed = parse_invite_token(token)
    if parsed == "expired":
        return {"status": "expired"}
    if not parsed:
        return {"status": "invalid"}

    invite = db.query(ProjectInvite).get(parsed["invite_id"])
    if not invite or invite.status != DBInviteStatus.pending:
        return {"status": "invalid"}

    masked = mask_email(invite.invitee_email)

    # Manually check auth header
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return {"status": "auth_required", "invitee_email_masked": masked}

    current_user = None
    if auth_header:
        try:
            token = auth_header.replace("Bearer ", "")
            credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
            current_user = get_current_user(credentials=credentials, db=db)
        except Exception:
            current_user = None

    if current_user.email.lower() != invite.invitee_email.lower():
        return {"status": "wrong_account", "invitee_email_masked": masked}

    return {"status": "ready_to_accept", "invitee_email_masked": masked}

@router.post("/project/invites/accept")
def accept_invite(
    token: str = Query(...),
    db: Session = Depends(get_db),
    current_user: TodoUsers = Depends(get_current_user),
):
    parsed = parse_invite_token(token)
    if parsed == "expired":
        raise HTTPException(410, "Invite token expired")
    if not parsed:
        raise HTTPException(400, "Invalid invite token")

    invite = db.query(ProjectInvite).get(parsed["invite_id"])
    if not invite or invite.status != DBInviteStatus.pending:
        raise HTTPException(400, "Invite is not valid anymore")
    if parsed["nonce"] != invite.token_nonce:
        raise HTTPException(400, "Invalid invite token")

    # email guard
    if current_user.email.lower() != invite.invitee_email.lower():
        raise HTTPException(403, f"This invite is for {mask_email(invite.invitee_email)}")

    project = invite.project
    # Add as collaborator if not already
    if current_user not in project.collaborators:
        project.collaborators.append(current_user)

    invite.status = DBInviteStatus.accepted
    db.commit()
    return {"status": "accepted"}

@router.post("/project/invites/decline")
def decline_invite(
    token: str = Query(...),
    db: Session = Depends(get_db),
):
    parsed = parse_invite_token(token)
    if parsed == "expired":
        inv = db.query(ProjectInvite).get(parsed["invite_id"])
        if inv and inv.status == DBInviteStatus.pending:
            inv.status = DBInviteStatus.expired
            db.commit()
        raise HTTPException(410, "Invite token expired")
    if not parsed:
        raise HTTPException(400, "Invalid invite token")

    invite = db.query(ProjectInvite).get(parsed["invite_id"])
    if not invite or invite.status != DBInviteStatus.pending:
        raise HTTPException(400, "Invite is not valid anymore")

    invite.status = DBInviteStatus.declined
    db.commit()
    return {"status": "declined"}

# Resend and revoke frontend implementation is remaining need to implement it in future.
@router.post("/project/{project_id}/invites/{invite_id}/resend")
def resend_invite(
    project_id: int,
    invite_id: int,
    db: Session = Depends(get_db),
    current_user: TodoUsers = Depends(get_current_user),
):
    invite = db.query(ProjectInvite).get(invite_id)
    if not invite or invite.project_id != project_id:
        raise HTTPException(404, "Invite not found")
    if invite.project.user_id != current_user.id:
        raise HTTPException(403, "Only the owner can resend invites")
    if invite.status != DBInviteStatus.pending:
        raise HTTPException(400, "Only pending invites can be resent")

    # Simple throttle (10 minutes)
    if invite.resent_at and (datetime.utcnow() - invite.resent_at) < timedelta(minutes=10):
        raise HTTPException(429, "Please wait before resending")

    token = make_invite_token(invite.id, invite.token_nonce)
    send_invite_email(invite.invitee_email, invite.project, token)
    invite.resent_at = datetime.utcnow()
    db.commit()
    return {"status": "resent"}

@router.delete("/project/{project_id}/invites/{invite_id}")
def revoke_invite(
    project_id: int,
    invite_id: int,
    db: Session = Depends(get_db),
    current_user: TodoUsers = Depends(get_current_user),
):
    invite = db.query(ProjectInvite).get(invite_id)
    if not invite or invite.project_id != project_id:
        raise HTTPException(404, "Invite not found")
    if invite.project.user_id != current_user.id:
        raise HTTPException(403, "Only the owner can revoke invites")
    if invite.status != DBInviteStatus.pending:
        raise HTTPException(400, "Only pending invites can be revoked")

    invite.status = DBInviteStatus.revoked
    db.commit()
    return {"status": "revoked"}
