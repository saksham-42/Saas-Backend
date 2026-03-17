from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class User_create(BaseModel):
    name : str = Field(min_length=2, max_length=20)
    age : int = Field(gt=18, lt=75)
    email : EmailStr

class Update_user(BaseModel):
    name : Optional[str] = None
    age : Optional[int] = None
    email : Optional[EmailStr] = None

class User_response(BaseModel):
    name : str
    age : int 
    email : EmailStr


