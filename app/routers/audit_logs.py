from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.db import get_database
from app.auth.dependencies import require_admin
from app.models.audit_log import AuditLog
from app.models.user import User
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/admin", tags=["audit-logs"])

@router.get("/audit-logs")
def get_audit_logs(
    user_id: Optional[int] = None,resource: Optional[str] = None,from_date: Optional[datetime] = Query(default=None, alias="from"),
    skip: int = 0,limit: int = 20,db: Session = Depends(get_database),_: User = Depends(require_admin)):
    "Return paginated audit logs — admin only. Filterable by user, resource, and date."
    query = db.query(AuditLog)
    if user_id:
        query = query.filter(AuditLog.user_id == user_id)
    if resource:
        query = query.filter(AuditLog.resource == resource)
    if from_date:
        query = query.filter(AuditLog.timestamp >= from_date)
    return query.order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit).all()