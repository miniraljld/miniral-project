from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class WaterQualityBase(BaseModel):
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    ph_level: Optional[float] = None
    chlorine_level: Optional[float] = None
    turbidity: Optional[float] = None
    temperature: Optional[float] = None
    dissolved_oxygen: Optional[float] = None
    e_coli: Optional[float] = None
    total_solids: Optional[float] = None
    chemical_oxygen_demand: Optional[float] = None
    biological_oxygen_demand: Optional[float] = None
    date_measured: datetime
    measured_by: Optional[str] = None
    notes: Optional[str] = None
    quality_status: str = "good"


class WaterQualityCreate(WaterQualityBase):
    pass


class WaterQualityUpdate(BaseModel):
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    ph_level: Optional[float] = None
    chlorine_level: Optional[float] = None
    turbidity: Optional[float] = None
    temperature: Optional[float] = None
    dissolved_oxygen: Optional[float] = None
    e_coli: Optional[float] = None
    total_solids: Optional[float] = None
    chemical_oxygen_demand: Optional[float] = None
    biological_oxygen_demand: Optional[float] = None
    date_measured: Optional[datetime] = None
    measured_by: Optional[str] = None
    notes: Optional[str] = None
    quality_status: Optional[str] = None


class WaterQualityResponse(WaterQualityBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class WaterQualityAlertBase(BaseModel):
    quality_id: int
    alert_type: str
    message: str
    is_active: bool = True
    acknowledged: bool = False
    acknowledged_by: Optional[int] = None
    acknowledged_at: Optional[datetime] = None


class WaterQualityAlertCreate(WaterQualityAlertBase):
    pass


class WaterQualityAlertUpdate(BaseModel):
    alert_type: Optional[str] = None
    message: Optional[str] = None
    is_active: Optional[bool] = None
    acknowledged: Optional[bool] = None
    acknowledged_by: Optional[int] = None
    acknowledged_at: Optional[datetime] = None


class WaterQualityAlertResponse(WaterQualityAlertBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True