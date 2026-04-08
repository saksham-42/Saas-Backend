from sqlalchemy.orm import Session
from app.core.db import get_database
from app.crud.users import get_user_by_email
from jose import JWTError, jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv
from app.models.user import User
from app.models.organization_member import OrganizationMember
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
    except JWTError as e:
        if "expired" in str(e):
            raise HTTPException(status_code=401, detail="Token has been expired")
        raise credentials_exception
    
    curr_user = get_user_by_email(db,email)
    if curr_user is None:
        raise credentials_exception
    return curr_user

def require_admin(current_user: User=Depends(get_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admins Only")
    return current_user

def get_org_member(org_id: int, curr_user: User=Depends(get_user), db: Session=Depends(get_database)):
    member = db.query(OrganizationMember).filter(OrganizationMember.org_id==org_id, OrganizationMember.user_id==curr_user.id).first()
    if not member:
        raise HTTPException(status_code=403, detail="Not a member of this organization")
    return member