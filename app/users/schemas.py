from typing import Optional
from fastapi_users import schemas
from uuid import UUID

from pydantic import UUID4, BaseModel, EmailStr


class UserRead(schemas.BaseUser[UUID4]):
    id: UUID
    email: EmailStr
    is_active: bool
    username: str

class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    password: str
    username: str

class UserUpdate(schemas.BaseUserUpdate):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    username: Optional[str] = None

class UserUpdateWithVerification(UserUpdate):
    is_verified: Optional[bool] = None 

class VerifyEmailRequest(BaseModel):
    token: str
    