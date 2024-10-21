from fastapi import APIRouter, Depends, HTTPException
from fastapi_users.exceptions import InvalidVerifyToken, UserAlreadyVerified

from app.users.auth_config import fastapi_users, auth_backend
from app.users.manager import UserManager, get_user_manager
from app.users.schemas import UserRead, UserCreate, UserUpdate, VerifyEmailRequest


router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"]
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"]
)

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"]
)

router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

@router.post("/auth/verify-email", tags=["auth"])
async def verify_email(request: VerifyEmailRequest, user_manager: UserManager = Depends(get_user_manager)):
    try:
        user = await user_manager.verify(request.token)
        return {"message": "Email успешно верифицирован"}
    except InvalidVerifyToken:
        raise HTTPException(status_code=400, detail="Неверный или истекший токен")
    except UserAlreadyVerified:
        raise HTTPException(status_code=400, detail="Пользователь уже верифицирован")
