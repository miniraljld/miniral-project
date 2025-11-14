from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.sql import func
from backend.config.database import Base


class Complaint(Base):
    """
    Модель для хранения жалоб и обращений пользователей
    """
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)  # ID пользователя (если авторизован)
    full_name = Column(String, nullable=False)  # Имя пользователя (если не авторизован)
    email = Column(String, nullable=True)  # Email пользователя
    phone = Column(String, nullable=True)  # Телефон пользователя
    category = Column(String, nullable=False)  # Категория жалобы (качество воды, утечка, санитария и т.д.)
    location = Column(String, nullable=True)  # Местоположение проблемы
    latitude = Column(Float, nullable=True)  # Широта
    longitude = Column(Float, nullable=True)  # Долгота
    description = Column(Text, nullable=False)  # Описание проблемы
    photo_url = Column(String, nullable=True)  # URL фото (если есть)
    priority = Column(String, default="medium")  # Приоритет (низкий, средний, высокий)
    status = Column(String, default="pending")  # Статус (ожидает, в процессе, решено)
    assigned_to = Column(Integer, nullable=True)  # ID пользователя, назначенного для решения
    resolved_at = Column(DateTime, nullable=True)  # Время решения
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ComplaintCategory(Base):
    """
    Модель для хранения категорий жалоб
    """
    __tablename__ = "complaint_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)  # Название категории
    description = Column(Text, nullable=True)  # Описание категории
    is_active = Column(Boolean, default=True)  # Активна ли категория
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())