from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SanitationFacilityBase(BaseModel):
    name: str
    type: str
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    capacity: Optional[int] = None
    is_accessible: bool = False
    is_operational: bool = True
    last_maintenance: Optional[datetime] = None
    condition_status: str = "good"
    installation_date: Optional[datetime] = None


class SanitationFacilityCreate(SanitationFacilityBase):
    pass


class SanitationFacilityUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    capacity: Optional[int] = None
    is_accessible: Optional[bool] = None
    is_operational: Optional[bool] = None
    last_maintenance: Optional[datetime] = None
    condition_status: Optional[str] = None
    installation_date: Optional[datetime] = None


class SanitationFacilityResponse(SanitationFacilityBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SanitationReportBase(BaseModel):
    facility_id: int
    reported_by: int
    report_date: datetime
    hygiene_rating: Optional[int] = None
    cleanliness_rating: Optional[int] = None
    accessibility_rating: Optional[int] = None
    description: Optional[str] = None
    photo_url: Optional[str] = None
    is_resolved: bool = False
    resolved_by: Optional[int] = None
    resolved_at: Optional[datetime] = None


class SanitationReportCreate(SanitationReportBase):
    pass


class SanitationReportUpdate(BaseModel):
    facility_id: Optional[int] = None
    reported_by: Optional[int] = None
    report_date: Optional[datetime] = None
    hygiene_rating: Optional[int] = None
    cleanliness_rating: Optional[int] = None
    accessibility_rating: Optional[int] = None
    description: Optional[str] = None
    photo_url: Optional[str] = None
    is_resolved: Optional[bool] = None
    resolved_by: Optional[int] = None
    resolved_at: Optional[datetime] = None


class SanitationReportResponse(SanitationReportBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True