from fastapi import FastAPI, Request
from app.routers import users, auth, organizations, tasks
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.middleware import RequestLoggingMiddleware
from app.core.logging import logger
from app.core.db import engine
import traceback

app = FastAPI()
app.add_middleware(RequestLoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"]
)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(organizations.router)
app.include_router(tasks.router)

@app.on_event("startup")
def app_on_startup():
    try:
        with engine.connect() as connection:
            logger.info("Database connected successfully")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        logger.error(f"Full traceback:\n{traceback.format_exc()}")
        raise


@app.exception_handler(404)
def not_found_error(request: Request, exc):
    return JSONResponse(status_code=404, content={"code": 404, "detail": "Resource not found"})


@app.exception_handler(RequestValidationError)
def validation_error_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={"code": 422, "detail": "Invalid request"})


@app.get("/")
def root():
    return {"message": "SaaS Backend is live!"}


@app.get("/health")
def health():
    return {"status": "ok"}
