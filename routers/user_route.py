from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import schemas
from models import TodoUsers
from crud import create_user, login_user
from dependency import get_db

router = APIRouter()

@router.post("/create/users", response_model=schemas.LoginResponse)
def create_user_route(user: schemas.UserBase, db: Session = Depends(get_db)):
    existing_user = db.query(TodoUsers).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists. Please try to login")
    new_user = create_user(db, user)
    return {
            "access_token": new_user["access_token"],
            "token_type": "bearer",
            "user": new_user["user"]
        }

@router.post("/login/user", response_model=schemas.LoginResponse)
def login_user_route(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    login_result = login_user(db, user_credentials)
    return {
        "access_token": login_result["access_token"],
        "token_type": "bearer",
        "user": login_result["user"]
    }
