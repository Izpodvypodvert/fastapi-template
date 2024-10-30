from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1 import routers_v1
from app.core.config import settings
from app.core.exceptions import ERROR_MESSAGES
from app.core.logger import logger
from starlette.middleware.sessions import SessionMiddleware


app = FastAPI()

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

for router in routers_v1:
    app.include_router(router, prefix="/v1")
 
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc):
    translated_detail = ERROR_MESSAGES.get(exc.detail, exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": translated_detail},
    )
