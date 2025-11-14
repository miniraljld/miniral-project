from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.sql import func
from backend.config.database import Base

from sqlalchemy import Enum
from enum import Enum as PyEnum

class UserRole(PyEnum):
    USER = "user"
    ENGINEER = "engineer"
    ADMIN = "admin"


class User(Base):
    """
    Модель пользователя для аутентификации и авторизации
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())