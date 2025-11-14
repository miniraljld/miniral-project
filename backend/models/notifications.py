from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from backend.config.database import Base


class Notification(Base):
    """
    Модель для хранения уведомлений пользователям
    """
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)  # ID пользователя (если уведомление персонализировано)
    title = Column(String, nullable=False)  # Заголовок уведомления
    message = Column(Text, nullable=False)  # Текст уведомления
    notification_type = Column(String, default="info")  # Тип уведомления (info, warning, alert)
    priority = Column(String, default="medium")  # Приоритет (low, medium, high)
    is_read = Column(Boolean, default=False)  # Прочитано ли уведомление
    target_audience = Column(String, default="all")  # Целевая аудитория (all, admin, user, specific_group)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class NotificationSetting(Base):
    """
    Модель для хранения настроек уведомлений пользователя
    """
    __tablename__ = "notification_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)  # ID пользователя
    notification_type = Column(String, nullable=False)  # Тип уведомления
    enabled = Column(Boolean, default=True)  # Включено ли уведомление
    channel_email = Column(Boolean, default=True)  # Уведомлять по email
    channel_sms = Column(Boolean, default=False)  # Уведомлять по SMS
    channel_push = Column(Boolean, default=True)  # Уведомлять через push-уведомления
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())