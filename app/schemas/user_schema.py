from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    username: str
    password: str

class UserResponse(BaseModel):
    success: bool
    message: str
    user_id: str
    token: str

class UserLogin(BaseModel):
    email: str
    password: str