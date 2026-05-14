from fastapi import APIRouter, Depends, Request, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.db import get_database
from app.schemas.user import User_create, User_response, Login
import app.services.auth_service as auth_service
from app.core.limiter import limiter, get_limit
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

def send_welcome_email(email: str):
    "Background task — logs welcome email (replace with real email service later)."
    logger.info("Welcome email sent to %s", email)

@router.post("/register", response_model=User_response)
@limiter.limit(get_limit("3/hour"))
def register(request: Request, user: User_create, background_tasks: BackgroundTasks , db: Session = Depends(get_database)):
    result = auth_service.register(user, db)
    background_tasks.add_task(send_welcome_email,user.email)
    return result

@router.post("/login")
@limiter.limit(get_limit("5/minute"))
def login(request: Request, user: Login, db: Session = Depends(get_database)):
    return auth_service.login(user, db)


@router.post("/refresh")
def refresh(refresh_token: str, db: Session = Depends(get_database)):
    return auth_service.refresh(refresh_token, db)


@router.post("/logout")
def logout(refresh_token: str, db: Session = Depends(get_database)):
    return auth_service.logout(refresh_token, db)
