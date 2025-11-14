from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.sql import func
from backend.config.database import Base


class Tariff(Base):
    """
    Модель для хранения информации о тарифах на водоснабжение
    """
    __tablename__ = "tariffs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Название тарифа
    description = Column(Text, nullable=True)  # Описание тарифа
    price_per_unit = Column(Float, nullable=False)  # Цена за единицу (например, за 1 м³)
    unit_type = Column(String, default="cubic_meter")  # Тип единицы измерения
    is_active = Column(Boolean, default=True)  # Активен ли тариф
    start_date = Column(DateTime, nullable=False)  # Дата начала действия тарифа
    end_date = Column(DateTime, nullable=True)  # Дата окончания действия тарифа
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class PaymentMethod(Base):
    """
    Модель для хранения способов оплаты
    """
    __tablename__ = "payment_methods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Название способа оплаты
    description = Column(Text, nullable=True)  # Описание способа оплаты
    is_active = Column(Boolean, default=True)  # Активен ли способ оплаты
    is_online = Column(Boolean, default=False)  # Онлайн ли способ оплаты
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class UserPayment(Base):
    """
    Модель для хранения информации о платежах пользователей
    """
    __tablename__ = "user_payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)  # ID пользователя
    amount = Column(Float, nullable=False)  # Сумма платежа
    tariff_id = Column(Integer, nullable=False)  # ID тарифа
    payment_method_id = Column(Integer, nullable=False)  # ID способа оплаты
    payment_date = Column(DateTime, nullable=False)  # Дата платежа
    payment_reference = Column(String, nullable=True)  # Ссылка/номер транзакции
    status = Column(String, default="completed")  # Статус платежа (completed, pending, failed)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())