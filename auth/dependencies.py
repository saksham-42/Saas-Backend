from sqlalchemy.orm import Session
from db import get_database
from crud.users import get_user_by_email
from jose import JWTError, jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_user(token : str = Depends(oauth_scheme), db: Session = Depends(get_database)):
    credentials_exception = HTTPException(status_code=401, detail="Could not validate the credentials")
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    curr_user = get_user_by_email(db,email)
    if curr_user is None:
        raise credentials_exception
    return curr_user



        