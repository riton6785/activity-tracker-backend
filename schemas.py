from pydantic import BaseModel
from datetime import date

class TodoBase(BaseModel):
    task: str
    completed: bool = False
    summary: str
    due_date: date
    finish_note: str | None

class TodoCreate(TodoBase):
    pass

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
