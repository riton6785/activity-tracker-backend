from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from utils import decode_access_token
from models import TodoUsers
from database import SessionLocal
oauth2_scheme = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    token = credentials.credentials  # Extract raw token string
    user_id = decode_access_token(token)
    user = db.query(TodoUsers).filter(TodoUsers.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user