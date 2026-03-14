from fastapi import FastAPI, Request
from routers import users
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.include_router(users.router)

app.add_middleware(
        CORSMiddleware,
        allow_origins = ["*"],
        allow_headers = ["*"],
        allow_methods = ["*"]
)

@app.exception_handler(404)
def not_found_error(request:Request, exc):
    return JSONResponse(status_code=404,content ={"code": 404, "detail": "Resource not found"})

@app.exception_handler(RequestValidationError)
def validation_error_handler(request:Request, exc : RequestValidationError):
    return JSONResponse(status_code= 422, content= {"code" : 422, "detail" : "Invalid request"})

@app.get("/")
def root():
    return {"message": "SaaS Backend is live!"}

@app.get("/health")
def health():
    return {"status": "ok"}