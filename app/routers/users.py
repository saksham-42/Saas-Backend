from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from app.schemas.user import User_response, User_create, Update_user
from app.schemas.task import Task_response
from app.core.db import get_database
import app.crud.users as crud
from app.auth.dependencies import get_user,require_admin
from app.models.user import User
import app.services.user_service as user_service

router = APIRouter(
    prefix = "/users",
    tags = ["users"]
)

@router.post("/", response_model= User_response)
def add_user(user : User_create, db:Session = Depends(get_database)):
    return user_service.add_user(user, db)

@router.get("/me", response_model=User_response)
def get_me(current_user : User = Depends(get_user)):
    return current_user

@router.get("/me/tasks", response_model=list[Task_response])
def get_my_tasks(skip: int =0, limit:int = 10, db:Session = Depends(get_database), curr_user: User = Depends(get_user)):
    return user_service.get_my_tasks(skip, limit, db, curr_user)

@router.get("/",response_model=list[User_response])
def get_all_users(db:Session = Depends(get_database), skip: int = 0, limit: int = 10, search: str = ""):
    return user_service.get_all_users(db, skip, limit, search)

@router.get("/{user_id}", response_model=User_response)
def get_user_by_id(user_id : int, db:Session = Depends(get_database)):
    return user_service.get_user_by_id(user_id, db)
    
@router.put("/{user_id}", response_model=User_response)
def update_user(user_id : int, user : Update_user, db : Session = Depends(get_database)):
    return user_service.update_user(user_id, user, db)

@router.delete("/{user_id}")
def delete_user(user_id : int, db: Session = Depends(get_database), curr_user : User = Depends(require_admin)):
    return user_service.delete_user(user_id, db, curr_user)

