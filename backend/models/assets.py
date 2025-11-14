from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.sql import func
from backend.config.database import Base


class WaterAsset(Base):
    """
    Модель для хранения информации об активах водоснабжения
    """
    __tablename__ = "water_assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Название актива
    asset_type = Column(String, nullable=False)  # Тип актива (труба, насос, резервуар и т.д.)
    description = Column(Text, nullable=True)  # Описание актива
    location = Column(String, nullable=False)  # Местоположение
    latitude = Column(Float, nullable=True)  # Широта
    longitude = Column(Float, nullable=True)  # Долгота
    installation_date = Column(DateTime, nullable=True)  # Дата установки
    last_maintenance = Column(DateTime, nullable=True)  # Дата последнего обслуживания
    next_maintenance = Column(DateTime, nullable=True)  # Дата следующего обслуживания
    status = Column(String, default="operational")  # Статус (работает, требует ремонта, выведен из эксплуатации)
    is_operational = Column(Boolean, default=True)  # Работает ли актив
    asset_value = Column(Float, nullable=True)  # Стоимость актива
    depreciation_rate = Column(Float, default=0.0)  # Ставка амортизации в год
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class AssetMaintenance(Base):
    """
    Модель для хранения истории обслуживания активов
    """
    __tablename__ = "asset_maintenance"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, nullable=False)  # ID актива
    maintenance_type = Column(String, nullable=False)  # Тип обслуживания (плановое, внеплановое, ремонт)
    description = Column(Text, nullable=True)  # Описание работ
    performed_by = Column(String, nullable=True)  # Кем выполнено обслуживание
    cost = Column(Float, nullable=True)  # Стоимость обслуживания
    maintenance_date = Column(DateTime, nullable=False)  # Дата обслуживания
    next_maintenance_date = Column(DateTime, nullable=True)  # Дата следующего обслуживания
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())