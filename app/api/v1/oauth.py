from fastapi import APIRouter, Request, Depends

from app.users.auth_config import get_user_manager
from app.users.manager import UserManager
from app.users.oauth_config import oauth
from app.users.service import generate_access_token, get_google_user_info, get_or_create_user


router = APIRouter(tags=["OAuth"])


@router.get("/auth/google/callback")
async def auth_google_callback(
    request: Request,
    user_manager: UserManager = Depends(get_user_manager),
    oauth_client = Depends(lambda: oauth)
):
    try:
        user_info = await get_google_user_info(request, oauth_client)
        user = await get_or_create_user(user_info, user_manager)
        access_token = await generate_access_token(user)
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    except Exception as e:
        return {"error": str(e)}


@router.get("/auth/google/login")
async def google_login(request: Request, oauth_client = Depends(lambda: oauth)):
    try:
        redirect_uri = request.url_for("auth_google_callback")
        return await oauth_client.google.authorize_redirect(request, redirect_uri)
    except Exception as e:
        return {"error": str(e)}
