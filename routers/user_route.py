from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import schemas
from models import TodoUsers, ProjectInvite
from crud import create_user, login_user
from dependency import get_db

router = APIRouter()

@router.post("/create/users", response_model=schemas.LoginResponse)
def create_user_route(user: schemas.UserBase, db: Session = Depends(get_db)):
    # 1. Check if user already exists
    existing_user = db.query(TodoUsers).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists. Please try to login")

    # 2. Create user with your existing function
    new_user_data = create_user(db, user)   # returns dict { access_token, user }

    # 3. Find pending invitations for this email
    pending_invitations = db.query(ProjectInvite).filter_by(
        invitee_email=user.email,
        status="pending"
    ).all()

    for invitation in pending_invitations:
        invitation.user_id = new_user_data["user"].id   # link invitation to new user
        invitation.status = "accepted"
        db.add(invitation)

    db.commit()
    return {
        "access_token": new_user_data["access_token"],
        "token_type": "bearer",
        "user": new_user_data["user"]
    }

@router.post("/login/user", response_model=schemas.LoginResponse)
def login_user_route(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    login_result = login_user(db, user_credentials)
    return {
        "access_token": login_result["access_token"],
        "token_type": "bearer",
        "user": login_result["user"]
    }
