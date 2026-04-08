from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional

class User_create(BaseModel):
    name : str = Field(min_length=2, max_length=20)
    age : int = Field(gt=15, lt=75)
    email : EmailStr
    password : str = Field(min_length=6)
    role : str = Field(default="member")

class Update_user(BaseModel):
    name : Optional[str] = Field(default=None, min_length=2, max_length=50)
    age : Optional[int] = Field(default=None, gt=15, lt=75)
    email : Optional[EmailStr] = None
    password : Optional[str] = Field(default=None, min_length=6)
    role : Optional[str] = None

class User_response(BaseModel):
    id : int
    name : str
    age : int 
    email : EmailStr
    role : str

    class Config:
        from_attributes = True

class Login(BaseModel):
    email: EmailStr
    password: str
