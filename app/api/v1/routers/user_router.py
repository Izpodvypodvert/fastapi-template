from fastapi import APIRouter, Depends, HTTPException
from fastapi_users.exceptions import InvalidVerifyToken, UserAlreadyVerified

from app.users.auth_config import fastapi_users, auth_backend, current_active_user
from app.users.manager import UserManager, get_user_manager
from app.users.models import User
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

@router.post("/auth/request-verification")
async def request_verification(
    user: User = Depends(current_active_user),  
    user_manager: UserManager = Depends(get_user_manager)
):
    if user.is_verified:
        raise HTTPException(status_code=400, detail="Пользователь уже верифицирован.")
    
    await user_manager.on_after_request_verify(user)

    return {"message": "Письмо для верификации отправлено повторно."}
