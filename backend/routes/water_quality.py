from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.config.database import get_db
from backend.models.water_quality import WaterQuality, WaterQualityAlert
from backend.schemas.water_quality import (
    WaterQualityCreate, 
    WaterQualityUpdate, 
    WaterQualityResponse,
    WaterQualityAlertCreate,
    WaterQualityAlertUpdate,
    WaterQualityAlertResponse
)

router = APIRouter()

@router.get("/", response_model=List[WaterQualityResponse])
def get_water_quality_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получить список данных о качестве воды
    """
    quality_data = db.query(WaterQuality).offset(skip).limit(limit).all()
    return quality_data


@router.post("/", response_model=WaterQualityResponse)
def create_water_quality_data(
    quality_data: WaterQualityCreate, 
    db: Session = Depends(get_db)
):
    """
    Создать новые данные о качестве воды
    """
    db_quality = WaterQuality(**quality_data.dict())
    db.add(db_quality)
    db.commit()
    db.refresh(db_quality)
    return db_quality


@router.get("/{quality_id}", response_model=WaterQualityResponse)
def get_water_quality_by_id(
    quality_id: int, 
    db: Session = Depends(get_db)
):
    """
    Получить данные о качестве воды по ID
    """
    quality = db.query(WaterQuality).filter(
        WaterQuality.id == quality_id
    ).first()
    if not quality:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Данные о качестве воды не найдены"
        )
    return quality


@router.put("/{quality_id}", response_model=WaterQualityResponse)
def update_water_quality(
    quality_id: int,
    quality_update: WaterQualityUpdate,
    db: Session = Depends(get_db)
):
    """
    Обновить данные о качестве воды
    """
    db_quality = db.query(WaterQuality).filter(
        WaterQuality.id == quality_id
    ).first()
    if not db_quality:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Данные о качестве воды не найдены"
        )
    
    update_data = quality_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_quality, field, value)
    
    db.commit()
    db.refresh(db_quality)
    return db_quality


@router.delete("/{quality_id}")
def delete_water_quality(
    quality_id: int, 
    db: Session = Depends(get_db)
):
    """
    Удалить данные о качестве воды
    """
    db_quality = db.query(WaterQuality).filter(
        WaterQuality.id == quality_id
    ).first()
    if not db_quality:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Данные о качестве воды не найдены"
        )
    
    db.delete(db_quality)
    db.commit()
    return {"message": "Данные о качестве воды успешно удалены"}


# Маршруты для уведомлений о качестве воды
@router.get("/alerts", response_model=List[WaterQualityAlertResponse])
def get_water_quality_alerts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получить список уведомлений о качестве воды
    """
    alerts = db.query(WaterQualityAlert).offset(skip).limit(limit).all()
    return alerts


@router.post("/alerts", response_model=WaterQualityAlertResponse)
def create_water_quality_alert(
    alert: WaterQualityAlertCreate, 
    db: Session = Depends(get_db)
):
    """
    Создать новое уведомление о качестве воды
    """
    db_alert = WaterQualityAlert(**alert.dict())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert


@router.patch("/alerts/{alert_id}/acknowledge")
def acknowledge_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):
    """
    Подтвердить уведомление о качестве воды
    """
    db_alert = db.query(WaterQualityAlert).filter(
        WaterQualityAlert.id == alert_id
    ).first()
    if not db_alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Уведомление не найдено"
        )
    
    db_alert.acknowledged = True
    db.commit()
    return {"message": "Уведомление подтверждено"}