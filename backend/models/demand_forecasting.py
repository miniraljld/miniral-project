from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.sql import func
from backend.config.database import Base


class WaterDemand(Base):
    """
    Модель для хранения данных о спросе на воду
    """
    __tablename__ = "water_demand"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, nullable=False)  # Местоположение
    latitude = Column(Float, nullable=True)  # Широта
    longitude = Column(Float, nullable=True)  # Долгота
    demand_amount = Column(Float, nullable=False)  # Объем спроса (в м³)
    demand_date = Column(DateTime, nullable=False)  # Дата спроса
    demand_type = Column(String, default="residential")  # Тип спроса (жилой, коммерческий, промышленный)
    forecasted = Column(Boolean, default=False)  # Является ли спрос прогнозируемым
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class WaterDistributionPlan(Base):
    """
    Модель для хранения планов распределения воды
    """
    __tablename__ = "water_distribution_plans"

    id = Column(Integer, primary_key=True, index=True)
    plan_name = Column(String, nullable=False)  # Название плана
    description = Column(Text, nullable=True)  # Описание плана
    start_date = Column(DateTime, nullable=False)  # Дата начала плана
    end_date = Column(DateTime, nullable=False)  # Дата окончания плана
    total_water_allocated = Column(Float, nullable=False)  # Общий объем выделенной воды
    allocated_to_residential = Column(Float, default=0.0)  # Объем для жилых нужд
    allocated_to_commercial = Column(Float, default=0.0)  # Объем для коммерческих нужд
    allocated_to_industrial = Column(Float, default=0.0)  # Объем для промышленных нужд
    allocated_to_public = Column(Float, default=0.0)  # Объем для общественных нужд
    status = Column(String, default="draft")  # Статус плана (черновик, утвержден, реализуется, завершен)
    created_by = Column(Integer, nullable=False)  # ID пользователя, создавшего план
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class InvestmentPlan(Base):
    """
    Модель для хранения инвестиционных планов
    """
    __tablename__ = "investment_plans"

    id = Column(Integer, primary_key=True, index=True)
    plan_name = Column(String, nullable=False)  # Название плана
    description = Column(Text, nullable=True)  # Описание плана
    total_investment = Column(Float, nullable=False)  # Общий объем инвестиций
    allocated_for_infrastructure = Column(Float, default=0.0)  # Инвестиции в инфраструктуру
    allocated_for_equipment = Column(Float, default=0.0)  # Инвестиции в оборудование
    allocated_for_maintenance = Column(Float, default=0.0)  # Инвестиции в обслуживание
    allocated_for_human_resources = Column(Float, default=0.0)  # Инвестиции в персонал
    start_date = Column(DateTime, nullable=False)  # Дата начала
    end_date = Column(DateTime, nullable=False)  # Дата окончания
    status = Column(String, default="planning")  # Статус плана (планирование, утвержден, реализуется, завершен)
    created_by = Column(Integer, nullable=False)  # ID пользователя, создавшего план
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())