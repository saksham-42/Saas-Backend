from fastapi import Depends, HTTPException, APIRouter
from schemas import User_response, User_create, Update_user
from db import get_database
from sqlalchemy.orm import Session
import crud.users as crud

router = APIRouter(
    prefix = "/users",
    tags = ["users"]
)

@router.get("/",response_model=list[User_response])
def get_all_users(db:Session = Depends(get_database), skip: int = 0, limit: int = 10, search: str = ""):
    return crud.get_users(db, skip = skip, limit = limit, search = search)

@router.get("/{user_id}", response_model=User_response)
def get_user(user_id : int, db:Session = Depends(get_database)):
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
def delete_user(user_id : int,db: Session = Depends(get_database)):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code= 404, detail="The user doesn't exist")
    crud.delete_user(db, user_id)
    return {"Success" : "User successfully deleted!"}