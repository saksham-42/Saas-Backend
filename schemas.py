from pydantic import BaseModel, EmailStr
from typing import Optional

class User_create(BaseModel):
    name : str
    age : int 
    email : EmailStr

class Update_user(BaseModel):
    name : Optional[str] = None
    age : Optional[int] = None
    email : Optional[EmailStr] = None

class User_response(BaseModel):
    name : str
    age : int 
    email : EmailStr


