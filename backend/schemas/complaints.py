from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ComplaintBase(BaseModel):
    user_id: Optional[int] = None
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    category: str
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: str
    photo_url: Optional[str] = None
    priority: str = "medium"
    status: str = "pending"
    assigned_to: Optional[int] = None
    resolved_at: Optional[datetime] = None


class ComplaintCreate(ComplaintBase):
    pass


class ComplaintUpdate(BaseModel):
    user_id: Optional[int] = None
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: Optional[str] = None
    photo_url: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    assigned_to: Optional[int] = None
    resolved_at: Optional[datetime] = None


class ComplaintResponse(ComplaintBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ComplaintCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True


class ComplaintCategoryCreate(ComplaintCategoryBase):
    pass


class ComplaintCategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class ComplaintCategoryResponse(ComplaintCategoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True