from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.config.database import get_db
from backend.models.water_infrastructure import WaterInfrastructure, WaterLeak
from backend.schemas.water_infrastructure import (
    WaterInfrastructureCreate, 
    WaterInfrastructureUpdate, 
    WaterInfrastructureResponse,
    WaterLeakCreate,
    WaterLeakUpdate,
    WaterLeakResponse
)

router = APIRouter()

@router.get("/", response_model=List[WaterInfrastructureResponse])
def get_water_infrastructure(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получить список объектов инфраструктуры водоснабжения
    """
    infrastructure = db.query(WaterInfrastructure).offset(skip).limit(limit).all()
    return infrastructure


@router.post("/", response_model=WaterInfrastructureResponse)
def create_water_infrastructure(
    infrastructure: WaterInfrastructureCreate, 
    db: Session = Depends(get_db)
):
    """
    Создать новый объект инфраструктуры водоснабжения
    """
    db_infrastructure = WaterInfrastructure(**infrastructure.dict())
    db.add(db_infrastructure)
    db.commit()
    db.refresh(db_infrastructure)
    return db_infrastructure


@router.get("/{infrastructure_id}", response_model=WaterInfrastructureResponse)
def get_water_infrastructure_by_id(
    infrastructure_id: int, 
    db: Session = Depends(get_db)
):
    """
    Получить объект инфраструктуры водоснабжения по ID
    """
    infrastructure = db.query(WaterInfrastructure).filter(
        WaterInfrastructure.id == infrastructure_id
    ).first()
    if not infrastructure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Объект инфраструктуры не найден"
        )
    return infrastructure


@router.put("/{infrastructure_id}", response_model=WaterInfrastructureResponse)
def update_water_infrastructure(
    infrastructure_id: int,
    infrastructure_update: WaterInfrastructureUpdate,
    db: Session = Depends(get_db)
):
    """
    Обновить объект инфраструктуры водоснабжения
    """
    db_infrastructure = db.query(WaterInfrastructure).filter(
        WaterInfrastructure.id == infrastructure_id
    ).first()
    if not db_infrastructure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Объект инфраструктуры не найден"
        )
    
    update_data = infrastructure_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_infrastructure, field, value)
    
    db.commit()
    db.refresh(db_infrastructure)
    return db_infrastructure


@router.delete("/{infrastructure_id}")
def delete_water_infrastructure(
    infrastructure_id: int, 
    db: Session = Depends(get_db)
):
    """
    Удалить объект инфраструктуры водоснабжения
    """
    db_infrastructure = db.query(WaterInfrastructure).filter(
        WaterInfrastructure.id == infrastructure_id
    ).first()
    if not db_infrastructure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Объект инфраструктуры не найден"
        )
    
    db.delete(db_infrastructure)
    db.commit()
    return {"message": "Объект инфраструктуры успешно удален"}


# Маршруты для утечек
@router.get("/{infrastructure_id}/leaks", response_model=List[WaterLeakResponse])
def get_leaks_by_infrastructure(
    infrastructure_id: int, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Получить список утечек для конкретного объекта инфраструктуры
    """
    leaks = db.query(WaterLeak).filter(
        WaterLeak.infrastructure_id == infrastructure_id
    ).offset(skip).limit(limit).all()
    return leaks


@router.post("/{infrastructure_id}/leaks", response_model=WaterLeakResponse)
def create_leak(
    infrastructure_id: int, 
    leak: WaterLeakCreate, 
    db: Session = Depends(get_db)
):
    """
    Создать новую утечку для объекта инфраструктуры
    """
    # Проверяем, существует ли объект инфраструктуры
    infrastructure = db.query(WaterInfrastructure).filter(
        WaterInfrastructure.id == infrastructure_id
    ).first()
    if not infrastructure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Объект инфраструктуры не найден"
        )
    
    db_leak = WaterLeak(
        infrastructure_id=infrastructure_id,
        **leak.dict()
    )
    db.add(db_leak)
    db.commit()
    db.refresh(db_leak)
    return db_leak