from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import TodoUsers
import schemas
from utils import hash_password, verify_password
from utils import create_access_token

def create_user(db: Session, user: schemas.UserBase):
    hashed_password = hash_password(user.password)
    create_user = TodoUsers(
        name = user.name, email=user.email, password=hashed_password, purpose=user.purpose, mobile_no=user.mobile_no
    )
    db.add(create_user)
    db.commit()
    db.refresh(create_user)
    access_token = create_access_token(data={"user_id": create_user.id})
    return {
        "access_token": access_token,
        "user": create_user  # SQLAlchemy object
    }

def login_user(db: Session, user: schemas.UserLogin):
    is_user_exists = db.query(TodoUsers).filter_by(email=user.email).first()
    if is_user_exists is None or not verify_password(user.password, is_user_exists.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"user_id": is_user_exists.id})
    return {
        "access_token": access_token,
        "user": is_user_exists  # SQLAlchemy object
    }