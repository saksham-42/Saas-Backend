from fastapi import HTTPException,APIRouter,Depends
from app.auth.hashing import hash_password, verify_password
from app.auth.tokens import create_access_token, create_refresh_token
from sqlalchemy.orm import Session
from app.core.db import get_database
from app.schemas.user import User_create,User_response,Login
from app.crud.users import get_user, get_user_by_email, create_user
from datetime import datetime, timedelta
from app.crud.refresh_tokens import get_refresh_token, revoke_refresh_token, save_refresh_token

router = APIRouter(
    prefix = "/auth",
    tags = ["auth"]
)

@router.post("/register",response_model=User_response)
def register(user : User_create, db : Session = Depends(get_database)):
    existing = get_user_by_email(db,user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db,user)

@router.post("/login")
def login(user:Login,db: Session = Depends(get_database)):
    db_user = get_user_by_email(db,user.email)
    if not db_user:
        raise HTTPException(status_code=401, detail= "Invalid credentials")
    if not verify_password(user.password,db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": db_user.email})
    refresh_token = create_refresh_token()
    save_refresh_token(db, refresh_token, db_user.id)
    return {"access_token":access_token,"refresh_token":refresh_token ,"token_type": "bearer"}

@router.post("/refresh")
def refresh(refresh_token:str, db: Session = Depends(get_database)):
    db_token = get_refresh_token(db, refresh_token)
    if not db_token or db_token.revoked:
        raise HTTPException(status_code=401 ,detail="Invalid or expired refresh token")
    access_token = create_access_token(data={"sub":db_token.user.email})
    return {"access_token": access_token, "token_type":"bearer"} 

@router.post("/logout")
def logout(refresh_token: str, db: Session = Depends(get_database)):
    revoke_refresh_token(db, refresh_token)
    return {"message": "Logged out successfully"}