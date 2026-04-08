from sqlalchemy.orm import Session
from app.models.refresh_token import RefreshToken
from datetime import datetime, timedelta,timezone

def save_refresh_token(db: Session, token: str, user_id: int):
    expires_at = datetime.now(timezone.utc)+timedelta(days=7)
    db_token = RefreshToken(token=token, user_id=user_id, expires_at= expires_at)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

def get_refresh_token(db: Session, token: str):
    return db.query(RefreshToken).filter(RefreshToken.token == token).first()

def revoke_refresh_token(db: Session, token: str):
    db_token = get_refresh_token(db, token)
    if db_token:
        db_token.revoked = True
        db.commit()

