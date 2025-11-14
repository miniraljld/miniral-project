from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.sql import func
from backend.config.database import Base


class SanitationFacility(Base):
    """
    Модель для хранения данных о санитарных сооружениях
    """
    __tablename__ = "sanitation_facilities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Название сооружения
    type = Column(String, nullable=False)  # Тип (туалет, душ, умывальник и т.д.)
    location = Column(String, nullable=False)  # Местоположение
    latitude = Column(Float, nullable=True)  # Широта
    longitude = Column(Float, nullable=True)  # Долгота
    capacity = Column(Integer, nullable=True)  # Вместимость
    is_accessible = Column(Boolean, default=False)  # Доступно ли для инвалидов
    is_operational = Column(Boolean, default=True)  # Работает ли сооружение
    last_maintenance = Column(DateTime, nullable=True)  # Дата последнего обслуживания
    condition_status = Column(String, default="good")  # Состояние (хорошее, удовлетворительное, требует ремонта)
    installation_date = Column(DateTime, nullable=True)  # Дата установки
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class SanitationReport(Base):
    """
    Модель для хранения отчетов о санитарии
    """
    __tablename__ = "sanitation_reports"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, nullable=False)  # ID сооружения
    reported_by = Column(Integer, nullable=False)  # ID пользователя, создавшего отчет
    report_date = Column(DateTime, nullable=False)  # Дата отчета
    hygiene_rating = Column(Integer, nullable=True)  # Рейтинг гигиены (1-5)
    cleanliness_rating = Column(Integer, nullable=True)  # Рейтинг чистоты (1-5)
    accessibility_rating = Column(Integer, nullable=True)  # Рейтинг доступности (1-5)
    description = Column(Text, nullable=True)  # Описание состояния
    photo_url = Column(String, nullable=True)  # URL фото (если есть)
    is_resolved = Column(Boolean, default=False)  # Решена ли проблема
    resolved_by = Column(Integer, nullable=True)  # ID пользователя, решившего проблему
    resolved_at = Column(DateTime, nullable=True)  # Время решения
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())