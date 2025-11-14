from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TariffBase(BaseModel):
    name: str
    description: Optional[str] = None
    price_per_unit: float
    unit_type: str = "cubic_meter"
    is_active: bool = True
    start_date: datetime
    end_date: Optional[datetime] = None


class TariffCreate(TariffBase):
    pass


class TariffUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price_per_unit: Optional[float] = None
    unit_type: Optional[str] = None
    is_active: Optional[bool] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class TariffResponse(TariffBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PaymentMethodBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True
    is_online: bool = False


class PaymentMethodCreate(PaymentMethodBase):
    pass


class PaymentMethodUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    is_online: Optional[bool] = None


class PaymentMethodResponse(PaymentMethodBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserPaymentBase(BaseModel):
    user_id: int
    amount: float
    tariff_id: int
    payment_method_id: int
    payment_date: datetime
    payment_reference: Optional[str] = None
    status: str = "completed"


class UserPaymentCreate(UserPaymentBase):
    pass


class UserPaymentUpdate(BaseModel):
    user_id: Optional[int] = None
    amount: Optional[float] = None
    tariff_id: Optional[int] = None
    payment_method_id: Optional[int] = None
    payment_date: Optional[datetime] = None
    payment_reference: Optional[str] = None
    status: Optional[str] = None


class UserPaymentResponse(UserPaymentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True