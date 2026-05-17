from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from app.core.db import SessionLocal
from app.crud.audit_log import create_log
import os

METHOD_ACTION_MAP = {
    "POST": "CREATE",
    "PUT": "UPDATE",
    "DELETE": "DELETE",
}


def _parse_resource(path: str):
    "Extract resource type and resource_id from URL path."
    parts = [p for p in path.strip("/").split("/") if p]
    resource = None
    resource_id = None
    for i, part in enumerate(parts):
        if not part.isdigit():
            resource = part
        else:
            resource_id = int(part)
    return resource, resource_id


class AuditLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        if os.getenv("TESTING") == "true":
            return response

        if request.method not in METHOD_ACTION_MAP:
            return response

        if response.status_code >= 400:
            return response

        action = METHOD_ACTION_MAP[request.method]
        resource, resource_id = _parse_resource(request.url.path)
        user_id = getattr(request.state, "user_id", None)
        org_id = getattr(request.state, "org_id", None)
        ip_address = request.client.host if request.client else None

        db = SessionLocal()
        try:
            create_log(db, action=action, resource=resource, user_id=user_id,
                       resource_id=resource_id, org_id=org_id, ip_address=ip_address)
        finally:
            db.close()

        return response