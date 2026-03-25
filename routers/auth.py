from fastapi import HTTPException,APIRouter,Depends
from auth.hashing import hash_password, verify_password
from auth.tokens import create_access_token
from sqlalchemy.orm import Session
from db import get_database
from schemas import User_create,User_response,Login
from crud.users import get_user, get_user_by_email, create_user

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
    return {"access_token":access_token,"token_type": "bearer"}
