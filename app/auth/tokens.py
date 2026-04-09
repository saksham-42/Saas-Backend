from jose import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import settings
import secrets

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc)+timedelta(minutes=settings.EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,settings.SECRET_KEY,algorithm=settings.ALGORITHM)

def create_refresh_token():
    return secrets.token_urlsafe(64)

