from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.sql import func
from backend.config.database import Base


class WaterQuality(Base):
    """
    Модель для хранения данных о качестве воды
    """
    __tablename__ = "water_quality"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, nullable=False)  # Местоположение точки измерения
    latitude = Column(Float, nullable=True)  # Широта
    longitude = Column(Float, nullable=True)  # Долгота
    ph_level = Column(Float, nullable=True)  # Уровень pH
    chlorine_level = Column(Float, nullable=True)  # Уровень хлора
    turbidity = Column(Float, nullable=True)  # Мутность
    temperature = Column(Float, nullable=True)  # Температура
    dissolved_oxygen = Column(Float, nullable=True)  # Растворенный кислород
    e_coli = Column(Float, nullable=True)  # Коли-бактерии
    total_solids = Column(Float, nullable=True)  # Общие твердые вещества
    chemical_oxygen_demand = Column(Float, nullable=True)  # Химическая потребность в кислороде
    biological_oxygen_demand = Column(Float, nullable=True)  # Биохимическая потребность в кислороде
    date_measured = Column(DateTime, nullable=False)  # Дата измерения
    measured_by = Column(String, nullable=True)  # Кем проведены измерения
    notes = Column(Text, nullable=True)  # Примечания
    quality_status = Column(String, default="good")  # Статус качества (хорошее, удовлетворительное, плохое)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class WaterQualityAlert(Base):
    """
    Модель для хранения уведомлений о качестве воды
    """
    __tablename__ = "water_quality_alerts"

    id = Column(Integer, primary_key=True, index=True)
    quality_id = Column(Integer, nullable=False)  # ID связанного измерения качества
    alert_type = Column(String, nullable=False)  # Тип уведомления (предупреждение, тревога)
    message = Column(Text, nullable=False)  # Сообщение уведомления
    is_active = Column(Boolean, default=True)  # Активно ли уведомление
    acknowledged = Column(Boolean, default=False)  # Подтверждено ли уведомление
    acknowledged_by = Column(Integer, nullable=True)  # ID пользователя, подтвердившего уведомление
    acknowledged_at = Column(DateTime, nullable=True)  # Время подтверждения
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())