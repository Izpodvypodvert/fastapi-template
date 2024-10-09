from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.user_router import router as user_router
from app.api.v1.oauth import router as oauth_router
from app.api.v1.todo import todo_router
from app.core.config import settings
from app.core.logger import logger
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

app.include_router(user_router)
app.include_router(oauth_router)
app.include_router(todo_router)

app.add_middleware(SessionMiddleware, secret_key=settings.secret)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    return response

@app.get("/")
async def root():
    return {"message": "Hello World"}