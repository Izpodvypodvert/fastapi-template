from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from app.api.v1.user_router import router as user_router

app = FastAPI()

app.include_router(user_router)

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