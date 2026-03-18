from sqlalchemy.orm import Session
from models.user import User
from schemas import User_response, User_create, Update_user

def get_users(db:Session, skip : int = 0, limit : int = 10):
    return db.query(User).offset(skip).limit(limit).all()

def get_user(db:Session,user_id:int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db:Session, email:str):
    return db.query(User).filter(User.email == email).first()

def create_user(db:Session, user : User_create):
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_user(db:Session, user_id : int, user :Update_user):
    db_user = get_user(db,user_id)
    if user.name is not None:
        db_user.name = user.name
    if user.email is not None:
        db_user.email = user.email
    if user.age is not None:
        db_user.age = user.age
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id : int):
    db_user = get_user(db,user_id)
    db.delete(db_user)
    db.commit()

