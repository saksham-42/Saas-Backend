from pydantic import BaseModel, Field
from typing import Optional

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

class Memb_role_update(BaseModel):
    role : str = Field(pattern ="member|admin")