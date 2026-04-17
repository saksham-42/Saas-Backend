from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import Update_user
import app.crud.users as crud
from app.models.task import Task


def get_my_tasks(skip: int, limit: int, db: Session, curr_user):
    "Return paginated list of non-deleted tasks assigned to the current user."
    tasks = db.query(Task).filter(Task.assigned_to == curr_user.id,
                                  Task.is_deleted.is_(False)).offset(skip).limit(limit).all()
    return tasks


def get_all_users(db: Session, skip: int, limit: int, search: str):
    "Return paginated list of users, optionally filtered by name search."
    return crud.get_users(db, skip=skip, limit=limit, search=search)


def get_user_by_id(user_id: int, db: Session):
    "Fetch a user by ID. Raises 404 if not found."
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User doesn't exist")
    return user


def update_user(user_id: int, user: Update_user, db: Session):
    "Update a user's details. Raises 404 if user not found."
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User doesn't exist")
    return crud.update_user(db, user_id, user)


def delete_user(user_id: int, db: Session, curr_user):
    "Delete a user account. Raises 404 if user not found."
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="The user doesn't exist")
    crud.delete_user(db, user_id)
    return {"Success": "User successfully deleted!"}
