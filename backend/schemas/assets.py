from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class WaterAssetBase(BaseModel):
    name: str
    asset_type: str
    description: Optional[str] = None
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    installation_date: Optional[datetime] = None
    last_maintenance: Optional[datetime] = None
    next_maintenance: Optional[datetime] = None
    status: str = "operational"
    is_operational: bool = True
    asset_value: Optional[float] = None
    depreciation_rate: float = 0.0


class WaterAssetCreate(WaterAssetBase):
    pass


class WaterAssetUpdate(BaseModel):
    name: Optional[str] = None
    asset_type: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    installation_date: Optional[datetime] = None
    last_maintenance: Optional[datetime] = None
    next_maintenance: Optional[datetime] = None
    status: Optional[str] = None
    is_operational: Optional[bool] = None
    asset_value: Optional[float] = None
    depreciation_rate: Optional[float] = None


class WaterAssetResponse(WaterAssetBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AssetMaintenanceBase(BaseModel):
    asset_id: int
    maintenance_type: str
    description: Optional[str] = None
    performed_by: Optional[str] = None
    cost: Optional[float] = None
    maintenance_date: datetime
    next_maintenance_date: Optional[datetime] = None


class AssetMaintenanceCreate(AssetMaintenanceBase):
    pass


class AssetMaintenanceUpdate(BaseModel):
    asset_id: Optional[int] = None
    maintenance_type: Optional[str] = None
    description: Optional[str] = None
    performed_by: Optional[str] = None
    cost: Optional[float] = None
    maintenance_date: Optional[datetime] = None
    next_maintenance_date: Optional[datetime] = None


class AssetMaintenanceResponse(AssetMaintenanceBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True