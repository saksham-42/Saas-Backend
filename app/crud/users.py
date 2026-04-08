from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import User_create, Update_user
from app.auth.hashing import hash_password

def get_users(db:Session, skip : int = 0, limit : int = 10,search:str=""):
    return db.query(User).filter(User.name.ilike(f"%{search}%")).offset(skip).limit(limit).all()

def get_user(db:Session,user_id:int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db:Session, email:str):
    return db.query(User).filter(User.email == email).first()

def create_user(db:Session, user : User_create):
    hashed = hash_password(user.password)
    user_data = user.model_dump(exclude={"password"})
    new_user = User(**user_data, hashed_password=hashed)
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
    if user.password is not None:
        db_user.hashed_password = hash_password(user.password)
    if user.role is not None:
        db_user.role = user.role
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id : int):
    db_user = get_user(db,user_id)
    db.expire(db_user, ['organization_members', 'refresh_tokens', 'tasks'])
    db.delete(db_user)
    db.commit()

