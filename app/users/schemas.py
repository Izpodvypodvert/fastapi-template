from typing import Optional
from fastapi_users import schemas
from uuid import UUID

from pydantic import UUID4, EmailStr


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
    username: str

