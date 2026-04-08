from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime, timezone
from enum import Enum

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

