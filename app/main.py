from fastapi import FastAPI, Request
from app.routers import users, auth, organizations, tasks, websockets, audit_logs
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.middleware import RequestLoggingMiddleware, SecurityHeadersMiddleware, RequestSizeLimitMiddleware
from app.core.logging import logger
from app.core.db import engine
from app.core.cache import get_redis
from app.core.limiter import limiter
from app.core.audit_middleware import AuditLogMiddleware
from sqlalchemy import text
from contextlib import asynccontextmanager
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
import traceback

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connected successfully")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        logger.error(f"Full traceback:\n{traceback.format_exc()}")
        raise

    
    yield

    # Shutdown
    get_redis().close()
    engine.dispose()
    logger.info("Database connections closed. Shutdown complete.")

app = FastAPI(lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(RequestSizeLimitMiddleware)
app.add_middleware(AuditLogMiddleware)
app.add_middleware(RequestLoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"]
)

app.add_middleware(SecurityHeadersMiddleware)

app.include_router(users.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(organizations.router, prefix="/api/v1")
app.include_router(tasks.router, prefix="/api/v1")
app.include_router(websockets.router, prefix="/api/v1")
app.include_router(audit_logs.router, prefix="/api/v1")


@app.exception_handler(404)
def not_found_error(request: Request, exc):
    return JSONResponse(status_code=404, content={"code": 404, "detail": "Resource not found"})


@app.exception_handler(RequestValidationError)
def validation_error_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={"code": 422, "detail": "Invalid request"})


@app.get("/")
def root():
    return {"message": "SaaS Backend is live!",
            "version": "v1"}


@app.get("/health")
def health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(status_code=503, content={"status": "degraded", "database": "unreachable"})