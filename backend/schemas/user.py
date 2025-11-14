from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from backend.models.user import UserRole


class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    role: Optional[UserRole] = UserRole.USER


class UserCreate(UserBase):
    password: str
    # Убираем возможность указать роль при создании - всегда будет USER по умолчанию
    role: UserRole = UserRole.USER


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[UserRole] = None


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True