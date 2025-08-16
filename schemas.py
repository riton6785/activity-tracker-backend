from pydantic import BaseModel
from datetime import date
from typing import Optional

class TodoBase(BaseModel):
    task: str
    completed: bool = False
    summary: str
    due_date: date
    finish_note: str | None

class TodoCreate(BaseModel):
    task: str
    completed: bool = False
    summary: str
    due_date: date

class TodoOut(TodoBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: str
    password: str

class UserBase(UserLogin):
    name: str
    mobile_no: str
    purpose: str

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    purpose: str
    mobile_no: str

    class Config:
        from_attributes = True

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut  # Nested object

    class Config:
        from_attributes = True

class ToggleNote(BaseModel):
    id: int
    notes: str

class EditActivities(BaseModel):
    id: int
    task: str
    summary: str
    due_date: date

# Project Schemas

class ProjectCreate(BaseModel):
    name: str
    description: str
    due_date: date
    completed: bool

class ProjectCreateOut(ProjectCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True


# Task Schemas

class TaskCreate(BaseModel):
    name: str
    description: str
    project_id: int
    # assignee_id: Optional[int] = None Need to add this in future when adding the collabortaor feature in project
    due_date: date
    completed: bool

class TaskCreateOut(TaskCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True
