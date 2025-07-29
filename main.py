from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas
from crud import create_todo, get_todo_by_id, get_todos, delete_todo, create_user, login_user, toggle_todo_completed
from models import TodoUsers
from database import SessionLocal, engine, Base
from utils import decode_access_token
from fastapi.openapi.utils import get_openapi

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
oauth2_scheme = HTTPBearer()

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()

bearer_scheme = HTTPBearer()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Todo api routes",
        version="1.0.0",
        description="API using HTTPBearer Token",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"HTTPBearer": []}])
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    token = credentials.credentials  # Extract raw token string
    user_id = decode_access_token(token)
    user = db.query(TodoUsers).filter(TodoUsers.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@app.get("/")
def root():
    return {"msg": "Todo API running"}

@app.post("/todos/", response_model=schemas.TodoOut)
def create_todo_route(todo: schemas.TodoCreate, db: Session = Depends(get_db), current_user: TodoUsers = Depends(get_current_user)):
    return create_todo(db, todo, current_user.id)

@app.get("/todos/", response_model=list[schemas.TodoOut], )
def read_todos(db: Session = Depends(get_db), current_user: TodoUsers = Depends(get_current_user)):
    return get_todos(db, current_user)

@app.get("/todos/{id}", response_model=schemas.TodoOut)
def read_todo(id: int, db: Session = Depends(get_db)):
    todo = get_todo_by_id(db, id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.delete("/todos/{id}")
def delete_todo_route(
    id: int,
    db: Session = Depends(get_db),
    current_user: TodoUsers = Depends(get_current_user)
):
    success = delete_todo(db, id, current_user)

    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Deleted successfully"}

@app.put("/todos/{id}/toggle", response_model=schemas.TodoOut)
def toggle_todo_route(
    id: int,
    db: Session = Depends(get_db),
    current_user: TodoUsers = Depends(get_current_user)
):
    updated_todo = toggle_todo_completed(db, id, current_user)
    if not updated_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated_todo

@app.post("/create/users", response_model=schemas.LoginResponse)
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

@app.post("/login/user", response_model=schemas.LoginResponse)
def login_user_route(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    login_result = login_user(db, user_credentials)
    return {
        "access_token": login_result["access_token"],
        "token_type": "bearer",
        "user": login_result["user"]
    }

