from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.core.db import get_database
from app.schemas.user import User_create,User_response,Login
import app.services.auth_service as auth_service

router = APIRouter(
    prefix = "/auth",
    tags = ["auth"]
)

@router.post("/register",response_model=User_response)
def register(user : User_create, db : Session = Depends(get_database)):
    return auth_service.register(user, db)

@router.post("/login")
def login(user:Login,db: Session = Depends(get_database)):
    return auth_service.login(user, db)

@router.post("/refresh")
def refresh(refresh_token:str, db: Session = Depends(get_database)):
    return auth_service.refresh(refresh_token, db)

@router.post("/logout")
def logout(refresh_token: str, db: Session = Depends(get_database)):
    return auth_service.logout(refresh_token, db)