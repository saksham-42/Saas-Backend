from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime, timezone
from enum import Enum

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

class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"

class Task_create(BaseModel):
    title : str = Field(min_length=2, max_length=50)
    description : Optional[str] = None
    status : TaskStatus = TaskStatus.pending
    priority : TaskPriority = TaskPriority.medium
    assigned_to : Optional[int] = None 
    due_date : Optional[datetime]
    
    @field_validator("due_date")
    @classmethod
    def due_date_must_be_future(cls, v):
        if v and v < datetime.now(timezone.utc):
            raise ValueError("due_date can't be in past")
        return v

class Task_response(BaseModel):
    id : int
    description : Optional[str]
    title : str
    status : str
    priority : str
    created_at : datetime
    is_deleted : bool
    org_id : int
    assigned_to : Optional[int]
    due_date : Optional[datetime]

    class Config:
        from_attributes = True
        
class TaskUpdate(BaseModel):
    status : TaskStatus

class TaskAssign(BaseModel):
    assigned_to : int

