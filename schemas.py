from pydantic import BaseModel

class TodoBase(BaseModel):
    task: str
    completed: bool = False

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

class UserOut(UserBase):
    id: int
    todos: list[TodoOut] = []

    class Config:
        from_attributes = True

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut  # Nested object

    class Config:
        from_attributes = True
