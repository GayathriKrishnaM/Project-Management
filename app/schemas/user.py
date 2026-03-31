from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    role: str = "developer"

class UserLogin(BaseModel):
    email: EmailStr    
