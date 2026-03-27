from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class User_create(BaseModel):
    name : str = Field(min_length=2, max_length=20)
    age : int = Field(gt=18, lt=75)
    email : EmailStr
    org_id : int
    password : str = Field(min_length=6)
    role : str = Field(min_length=5)

class Update_user(BaseModel):
    name : Optional[str] = Field(default=None, min_length=2, max_length=50)
    age : Optional[int] = Field(default=None, gt=15, lt=75)
    email : Optional[EmailStr] = None

class User_response(BaseModel):
    id : int
    name : str
    age : int 
    email : EmailStr

    class Config:
        from_attributes = True


class Login(BaseModel):
    email: EmailStr
    password: str