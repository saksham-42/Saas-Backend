import time
import uuid
import traceback
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logging import logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())[:8]
        request.state.request_id = request_id

        start_time = time.time()

        logger.info(f"[{request_id}] {request.method} {request.url.path} — started")

        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(
                f"[{request_id}] {request.method} {request.url.path} — unhandled error: {e}\n{traceback.format_exc()}"
            )
            raise

        duration = (time.time() - start_time) * 1000
        logger.info(f"[{request_id}] {request.method} {request.url.path} — {response.status_code} — {duration:.1f}ms")

        response.headers["X-Request-ID"] = request_id
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["X-Frame-Options"] = "DENY"
        return response


class RequestSizeLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.headers.get("content-length"):
            if int(request.headers["content-length"]) > 1_000_000:
                return JSONResponse(status_code=413, content={"detail": "Request too large"})
        return await call_next(request)