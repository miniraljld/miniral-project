from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class WaterInfrastructureBase(BaseModel):
    name: str
    type: str
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    pressure: Optional[float] = None
    temperature: Optional[float] = None
    leak_detected: bool = False
    last_inspection: Optional[datetime] = None
    condition_status: str = "good"
    installation_date: Optional[datetime] = None


class WaterInfrastructureCreate(WaterInfrastructureBase):
    pass


class WaterInfrastructureUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    pressure: Optional[float] = None
    temperature: Optional[float] = None
    leak_detected: Optional[bool] = None
    last_inspection: Optional[datetime] = None
    condition_status: Optional[str] = None
    installation_date: Optional[datetime] = None


class WaterInfrastructureResponse(WaterInfrastructureBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class WaterLeakBase(BaseModel):
    infrastructure_id: int
    leak_detected_at: datetime
    severity: str = "low"
    description: Optional[str] = None
    repaired: bool = False
    repair_date: Optional[datetime] = None


class WaterLeakCreate(WaterLeakBase):
    pass


class WaterLeakUpdate(BaseModel):
    leak_detected_at: Optional[datetime] = None
    severity: Optional[str] = None
    description: Optional[str] = None
    repaired: Optional[bool] = None
    repair_date: Optional[datetime] = None


class WaterLeakResponse(WaterLeakBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True