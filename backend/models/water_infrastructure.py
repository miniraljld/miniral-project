from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.sql import func
from backend.config.database import Base


class WaterInfrastructure(Base):
    """
    Модель для хранения данных об инфраструктуре водоснабжения
    """
    __tablename__ = "water_infrastructure"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Название объекта
    type = Column(String, nullable=False)  # Тип объекта (труба, насосная станция, резервуар и т.д.)
    location = Column(String, nullable=False)  # Местоположение
    latitude = Column(Float, nullable=True)  # Широта
    longitude = Column(Float, nullable=True)  # Долгота
    pressure = Column(Float, nullable=True)  # Давление
    temperature = Column(Float, nullable=True)  # Температура
    leak_detected = Column(Boolean, default=False)  # Обнаружена ли утечка
    last_inspection = Column(DateTime, nullable=True)  # Дата последнего осмотра
    condition_status = Column(String, default="good")  # Состояние (хорошее, удовлетворительное, требует ремонта)
    installation_date = Column(DateTime, nullable=True)  # Дата установки
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class WaterLeak(Base):
    """
    Модель для хранения данных об утечках воды
    """
    __tablename__ = "water_leaks"

    id = Column(Integer, primary_key=True, index=True)
    infrastructure_id = Column(Integer, nullable=False)  # ID объекта инфраструктуры
    leak_detected_at = Column(DateTime, nullable=False)  # Время обнаружения утечки
    severity = Column(String, default="low")  # Степень утечки (низкая, средняя, высокая)
    description = Column(Text, nullable=True)  # Описание утечки
    repaired = Column(Boolean, default=False)  # Устранена ли утечка
    repair_date = Column(DateTime, nullable=True)  # Дата устранения
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())