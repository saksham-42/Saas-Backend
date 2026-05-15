from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog
from datetime import datetime, timezone


def create_log(db: Session, action: str, resource: str, user_id: int = None,
               resource_id: int = None, org_id: int = None, ip_address: str = None):
    "Insert a single audit log entry into the database."
    log = AuditLog(
        user_id=user_id,
        action=action,
        resource=resource,
        resource_id=resource_id,
        org_id=org_id,
        ip_address=ip_address,
        timestamp=datetime.now(timezone.utc)
    )
    db.add(log)
    db.commit()