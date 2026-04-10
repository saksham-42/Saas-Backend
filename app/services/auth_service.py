from fastapi import HTTPException
from app.auth.hashing import verify_password
from app.auth.tokens import create_access_token, create_refresh_token
from sqlalchemy.orm import Session
from app.schemas.user import User_create,Login
from app.crud.users import get_user_by_email, create_user
from app.crud.refresh_tokens import get_refresh_token, revoke_refresh_token, save_refresh_token

def register(user : User_create, db : Session ):
    existing = get_user_by_email(db,user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db,user)

def login(user:Login,db: Session ):
    db_user = get_user_by_email(db,user.email)
    if not db_user:
        raise HTTPException(status_code=401, detail= "Invalid credentials")
    if not verify_password(user.password,db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": db_user.email})
    refresh_token = create_refresh_token()
    save_refresh_token(db, refresh_token, db_user.id)
    return {"access_token":access_token,"refresh_token":refresh_token ,"token_type": "bearer"}

def refresh(refresh_token:str, db: Session ):
    db_token = get_refresh_token(db, refresh_token)
    if not db_token or db_token.revoked:
        raise HTTPException(status_code=401 ,detail="Invalid or expired refresh token")
    access_token = create_access_token(data={"sub":db_token.user.email})
    return {"access_token": access_token, "token_type":"bearer"} 

def logout(refresh_token: str, db: Session ):
    revoke_refresh_token(db, refresh_token)
    return {"message": "Logged out successfully"}