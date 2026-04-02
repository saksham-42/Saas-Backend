from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class User_create(BaseModel):
    name : str = Field(min_length=2, max_length=20)
    age : int = Field(gt=18, lt=75)
    email : EmailStr
    org_id : Optional[int] = None
    password : str = Field(min_length=6)
    role : str = Field(min_length=5)    

class Update_user(BaseModel):
    name : Optional[str] = Field(default=None, min_length=2, max_length=50)
    age : Optional[int] = Field(default=None, gt=15, lt=75)
    email : Optional[EmailStr] = None
    org_id : Optional[int] = None
    password : Optional[str] = Field(default=None, min_length=6)
    role : Optional[str] = Field(default=None, min_length=5)

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


class Org_create(BaseModel):
    name : str = Field(min_length=2, max_length=50)
    slug : str = Field(min_length=2, max_length=50)


class Org_response(BaseModel):
    id: int
    name: str
    slug: str
    owner_id: int

    class Config:
        from_attributes = True


class Task_create(BaseModel):
    title : str = Field(min_length=2, max_length=50)
    description : Optional[str] = None
    status : str = Field(default="pending")
    assigned_to : Optional[int] = None 

class Task_response(BaseModel):
    id : int
    description : Optional[str]
    title : str
    status : str
    created_at : datetime
    is_deleted : bool
    org_id : int
    assigned_to : Optional[int]

    class Config:
        from_attributes = True
        