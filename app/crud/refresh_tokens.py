from sqlalchemy.orm import Session
from app.models.refresh_token import RefreshToken
from datetime import datetime, timedelta, timezone


def save_refresh_token(db: Session, token: str, user_id: int):
    "Save a new refresh token for a user with a 7 day expiry."
    expires_at = datetime.now(timezone.utc) + timedelta(days=7)
    db_token = RefreshToken(token=token, user_id=user_id, expires_at=expires_at)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


def get_refresh_token(db: Session, token: str):
    "Fetch a refresh token record by token string. Returns None if not found."
    return db.query(RefreshToken).filter(RefreshToken.token == token).first()


def revoke_refresh_token(db: Session, token: str):
    "Mark a refresh token as revoked. No-op if token doesn't exist."
    db_token = get_refresh_token(db, token)
    if db_token:
        db_token.revoked = True
        db.commit()
