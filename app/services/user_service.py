from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import User_create, Update_user
import app.crud.users as crud
from app.models.user import User
from app.models.task import Task

def add_user(user : User_create, db:Session ):
    existing = crud.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db,user)

def get_my_tasks(skip: int, limit: int, db :Session, curr_user):
    tasks = db.query(Task).filter(Task.assigned_to==curr_user.id, Task.is_deleted==False).offset(skip).limit(limit).all()
    return tasks

def get_all_users(db:Session , skip: int , limit: int , search: str):
    return crud.get_users(db, skip = skip, limit = limit, search = search)

def get_user_by_id(user_id: int, db:Session):
    user = crud.get_user(db,user_id)
    if not user:
        raise HTTPException(status_code = 404, detail="User doesn't exist")
    return user
    
def update_user(user_id : int, user : Update_user, db : Session):
    db_user = crud.get_user(db,user_id)
    if not db_user:
        raise HTTPException(status_code= 404, detail="User doesn't exist")
    return crud.update_user(db, user_id, user)

def delete_user(user_id : int, db: Session, curr_user):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code= 404, detail="The user doesn't exist")
    crud.delete_user(db, user_id)
    return {"Success" : "User successfully deleted!"}

