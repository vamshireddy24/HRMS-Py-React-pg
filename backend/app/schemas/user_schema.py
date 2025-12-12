# app/schemas/user_schema.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    

class UserOut(BaseModel):
    id: str
    email: EmailStr
    name: str

    class Config:
        orm_mode = True
