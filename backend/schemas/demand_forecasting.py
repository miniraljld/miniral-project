from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class WaterDemandBase(BaseModel):
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    demand_amount: float
    demand_date: datetime
    demand_type: str = "residential"
    forecasted: bool = False


class WaterDemandCreate(WaterDemandBase):
    pass


class WaterDemandUpdate(BaseModel):
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    demand_amount: Optional[float] = None
    demand_date: Optional[datetime] = None
    demand_type: Optional[str] = None
    forecasted: Optional[bool] = None


class WaterDemandResponse(WaterDemandBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class WaterDistributionPlanBase(BaseModel):
    plan_name: str
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    total_water_allocated: float
    allocated_to_residential: float = 0.0
    allocated_to_commercial: float = 0.0
    allocated_to_industrial: float = 0.0
    allocated_to_public: float = 0.0
    status: str = "draft"
    created_by: int


class WaterDistributionPlanCreate(WaterDistributionPlanBase):
    pass


class WaterDistributionPlanUpdate(BaseModel):
    plan_name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    total_water_allocated: Optional[float] = None
    allocated_to_residential: Optional[float] = None
    allocated_to_commercial: Optional[float] = None
    allocated_to_industrial: Optional[float] = None
    allocated_to_public: Optional[float] = None
    status: Optional[str] = None
    created_by: Optional[int] = None


class WaterDistributionPlanResponse(WaterDistributionPlanBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class InvestmentPlanBase(BaseModel):
    plan_name: str
    description: Optional[str] = None
    total_investment: float
    allocated_for_infrastructure: float = 0.0
    allocated_for_equipment: float = 0.0
    allocated_for_maintenance: float = 0.0
    allocated_for_human_resources: float = 0.0
    start_date: datetime
    end_date: datetime
    status: str = "planning"
    created_by: int


class InvestmentPlanCreate(InvestmentPlanBase):
    pass


class InvestmentPlanUpdate(BaseModel):
    plan_name: Optional[str] = None
    description: Optional[str] = None
    total_investment: Optional[float] = None
    allocated_for_infrastructure: Optional[float] = None
    allocated_for_equipment: Optional[float] = None
    allocated_for_maintenance: Optional[float] = None
    allocated_for_human_resources: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[str] = None
    created_by: Optional[int] = None


class InvestmentPlanResponse(InvestmentPlanBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True