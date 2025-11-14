from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class NotificationBase(BaseModel):
    user_id: Optional[int] = None
    title: str
    message: str
    notification_type: str = "info"
    priority: str = "medium"
    is_read: bool = False
    target_audience: str = "all"


class NotificationCreate(NotificationBase):
    pass


class NotificationUpdate(BaseModel):
    user_id: Optional[int] = None
    title: Optional[str] = None
    message: Optional[str] = None
    notification_type: Optional[str] = None
    priority: Optional[str] = None
    is_read: Optional[bool] = None
    target_audience: Optional[str] = None


class NotificationResponse(NotificationBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class NotificationSettingBase(BaseModel):
    user_id: int
    notification_type: str
    enabled: bool = True
    channel_email: bool = True
    channel_sms: bool = False
    channel_push: bool = True


class NotificationSettingCreate(NotificationSettingBase):
    pass


class NotificationSettingUpdate(BaseModel):
    user_id: Optional[int] = None
    notification_type: Optional[str] = None
    enabled: Optional[bool] = None
    channel_email: Optional[bool] = None
    channel_sms: Optional[bool] = None
    channel_push: Optional[bool] = None


class NotificationSettingResponse(NotificationSettingBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True