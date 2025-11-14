from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.config.database import get_db
from backend.models.demand_forecasting import WaterDemand, WaterDistributionPlan, InvestmentPlan
from backend.schemas.demand_forecasting import (
    WaterDemandCreate, 
    WaterDemandUpdate, 
    WaterDemandResponse,
    WaterDistributionPlanCreate,
    WaterDistributionPlanUpdate,
    WaterDistributionPlanResponse,
    InvestmentPlanCreate,
    InvestmentPlanUpdate,
    InvestmentPlanResponse
)

router = APIRouter()

# Маршруты для данных о спросе
@router.get("/", response_model=List[WaterDemandResponse])
def get_water_demand_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получить список данных о спросе на воду
    """
    demand_data = db.query(WaterDemand).offset(skip).limit(limit).all()
    return demand_data


@router.post("/", response_model=WaterDemandResponse)
def create_water_demand_data(
    demand_data: WaterDemandCreate, 
    db: Session = Depends(get_db)
):
    """
    Создать новые данные о спросе на воду
    """
    db_demand = WaterDemand(**demand_data.dict())
    db.add(db_demand)
    db.commit()
    db.refresh(db_demand)
    return db_demand


@router.get("/{demand_id}", response_model=WaterDemandResponse)
def get_water_demand_by_id(
    demand_id: int, 
    db: Session = Depends(get_db)
):
    """
    Получить данные о спросе на воду по ID
    """
    demand = db.query(WaterDemand).filter(
        WaterDemand.id == demand_id
    ).first()
    if not demand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Данные о спросе не найдены"
        )
    return demand


@router.put("/{demand_id}", response_model=WaterDemandResponse)
def update_water_demand(
    demand_id: int,
    demand_update: WaterDemandUpdate,
    db: Session = Depends(get_db)
):
    """
    Обновить данные о спросе на воду
    """
    db_demand = db.query(WaterDemand).filter(
        WaterDemand.id == demand_id
    ).first()
    if not db_demand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Данные о спросе не найдены"
        )
    
    update_data = demand_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_demand, field, value)
    
    db.commit()
    db.refresh(db_demand)
    return db_demand


@router.delete("/{demand_id}")
def delete_water_demand(
    demand_id: int, 
    db: Session = Depends(get_db)
):
    """
    Удалить данные о спросе на воду
    """
    db_demand = db.query(WaterDemand).filter(
        WaterDemand.id == demand_id
    ).first()
    if not db_demand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Данные о спросе не найдены"
        )
    
    db.delete(db_demand)
    db.commit()
    return {"message": "Данные о спросе успешно удалены"}


# Маршруты для планов распределения воды
@router.get("/distribution-plans", response_model=List[WaterDistributionPlanResponse])
def get_distribution_plans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получить список планов распределения воды
    """
    plans = db.query(WaterDistributionPlan).offset(skip).limit(limit).all()
    return plans


@router.post("/distribution-plans", response_model=WaterDistributionPlanResponse)
def create_distribution_plan(
    plan: WaterDistributionPlanCreate, 
    db: Session = Depends(get_db)
):
    """
    Создать новый план распределения воды
    """
    db_plan = WaterDistributionPlan(**plan.dict())
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan


@router.get("/distribution-plans/{plan_id}", response_model=WaterDistributionPlanResponse)
def get_distribution_plan_by_id(
    plan_id: int, 
    db: Session = Depends(get_db)
):
    """
    Получить план распределения воды по ID
    """
    plan = db.query(WaterDistributionPlan).filter(
        WaterDistributionPlan.id == plan_id
    ).first()
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="План распределения не найден"
        )
    return plan


@router.put("/distribution-plans/{plan_id}", response_model=WaterDistributionPlanResponse)
def update_distribution_plan(
    plan_id: int,
    plan_update: WaterDistributionPlanUpdate,
    db: Session = Depends(get_db)
):
    """
    Обновить план распределения воды
    """
    db_plan = db.query(WaterDistributionPlan).filter(
        WaterDistributionPlan.id == plan_id
    ).first()
    if not db_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="План распределения не найден"
        )
    
    update_data = plan_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_plan, field, value)
    
    db.commit()
    db.refresh(db_plan)
    return db_plan


# Маршруты для инвестиционных планов
@router.get("/investment-plans", response_model=List[InvestmentPlanResponse])
def get_investment_plans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получить список инвестиционных планов
    """
    plans = db.query(InvestmentPlan).offset(skip).limit(limit).all()
    return plans


@router.post("/investment-plans", response_model=InvestmentPlanResponse)
def create_investment_plan(
    plan: InvestmentPlanCreate, 
    db: Session = Depends(get_db)
):
    """
    Создать новый инвестиционный план
    """
    db_plan = InvestmentPlan(**plan.dict())
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan


@router.get("/investment-plans/{plan_id}", response_model=InvestmentPlanResponse)
def get_investment_plan_by_id(
    plan_id: int, 
    db: Session = Depends(get_db)
):
    """
    Получить инвестиционный план по ID
    """
    plan = db.query(InvestmentPlan).filter(
        InvestmentPlan.id == plan_id
    ).first()
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Инвестиционный план не найден"
        )
    return plan


@router.put("/investment-plans/{plan_id}", response_model=InvestmentPlanResponse)
def update_investment_plan(
    plan_id: int,
    plan_update: InvestmentPlanUpdate,
    db: Session = Depends(get_db)
):
    """
    Обновить инвестиционный план
    """
    db_plan = db.query(InvestmentPlan).filter(
        InvestmentPlan.id == plan_id
    ).first()
    if not db_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Инвестиционный план не найден"
        )
    
    update_data = plan_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_plan, field, value)
    
    db.commit()
    db.refresh(db_plan)
    return db_plan


# Маршрут для прогноза спроса
@router.get("/forecast", response_model=List[WaterDemandResponse])
def get_demand_forecast(
    location: str = None,
    date_from: str = None,
    date_to: str = None,
    db: Session = Depends(get_db)
):
    """
    Получить прогноз спроса на основе исторических данных
    """
    query = db.query(WaterDemand)
    
    if location:
        query = query.filter(WaterDemand.location == location)
    if date_from:
        from datetime import datetime
        query = query.filter(WaterDemand.demand_date >= datetime.fromisoformat(date_from))
    if date_to:
        from datetime import datetime
        query = query.filter(WaterDemand.demand_date <= datetime.fromisoformat(date_to))
    
    forecast_data = query.all()
    return forecast_data