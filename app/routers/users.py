from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.schemas.user import User_response, User_create, Update_user
from app.schemas.task import Task_response
from app.core.db import get_database
import app.crud.users as crud
from app.auth.dependencies import get_user,require_admin
from app.models.user import User
from app.models.task import Task

router = APIRouter(
    prefix = "/users",
    tags = ["users"]
)

@router.get("/me", response_model=User_response)
def get_me(current_user : User = Depends(get_user)):
    return current_user

@router.get("/me/tasks", response_model=list[Task_response])
def get_my_tasks(skip: int =0, limit:int = 10, db:Session = Depends(get_database), curr_user: User = Depends(get_user)):
    tasks = db.query(Task).filter(Task.assigned_to==curr_user.id, Task.is_deleted==False).offset(skip).limit(limit).all()
    return tasks

@router.get("/",response_model=list[User_response])
def get_all_users(db:Session = Depends(get_database), skip: int = 0, limit: int = 10, search: str = ""):
    return crud.get_users(db, skip = skip, limit = limit, search = search)

@router.get("/{user_id}", response_model=User_response)
def get_user_by_id(user_id : int, db:Session = Depends(get_database)):
    user = crud.get_user(db,user_id)
    if not user:
        raise HTTPException(status_code = 404, detail="User doesn't exist")
    return user

@router.post("/", response_model= User_response)
def add_user(user : User_create, db:Session = Depends(get_database)):
    existing = crud.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db,user)
    
@router.put("/{user_id}", response_model=User_response)
def update_user(user_id : int, user : Update_user, db : Session = Depends(get_database)):
    db_user = crud.get_user(db,user_id)
    if not db_user:
        raise HTTPException(status_code= 404, detail="User doesn't exist")
    return crud.update_user(db, user_id, user)

@router.delete("/{user_id}")
def delete_user(user_id : int, db: Session = Depends(get_database), curr_user : User = Depends(require_admin)):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code= 404, detail="The user doesn't exist")
    crud.delete_user(db, user_id)
    return {"Success" : "User successfully deleted!"}

