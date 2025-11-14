from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.config.database import get_db
from backend.models.assets import WaterAsset, AssetMaintenance
from backend.schemas.assets import (
    WaterAssetCreate, 
    WaterAssetUpdate, 
    WaterAssetResponse,
    AssetMaintenanceCreate,
    AssetMaintenanceUpdate,
    AssetMaintenanceResponse
)

router = APIRouter()

# Маршруты для активов водоснабжения
@router.get("/", response_model=List[WaterAssetResponse])
def get_water_assets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получить список активов водоснабжения
    """
    assets = db.query(WaterAsset).offset(skip).limit(limit).all()
    return assets


@router.post("/", response_model=WaterAssetResponse)
def create_water_asset(
    asset: WaterAssetCreate, 
    db: Session = Depends(get_db)
):
    """
    Создать новый актив водоснабжения
    """
    db_asset = WaterAsset(**asset.dict())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset


@router.get("/{asset_id}", response_model=WaterAssetResponse)
def get_water_asset_by_id(
    asset_id: int, 
    db: Session = Depends(get_db)
):
    """
    Получить актив водоснабжения по ID
    """
    asset = db.query(WaterAsset).filter(
        WaterAsset.id == asset_id
    ).first()
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Актив водоснабжения не найден"
        )
    return asset


@router.put("/{asset_id}", response_model=WaterAssetResponse)
def update_water_asset(
    asset_id: int,
    asset_update: WaterAssetUpdate,
    db: Session = Depends(get_db)
):
    """
    Обновить актив водоснабжения
    """
    db_asset = db.query(WaterAsset).filter(
        WaterAsset.id == asset_id
    ).first()
    if not db_asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Актив водоснабжения не найден"
        )
    
    update_data = asset_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_asset, field, value)
    
    db.commit()
    db.refresh(db_asset)
    return db_asset


@router.delete("/{asset_id}")
def delete_water_asset(
    asset_id: int, 
    db: Session = Depends(get_db)
):
    """
    Удалить актив водоснабжения
    """
    db_asset = db.query(WaterAsset).filter(
        WaterAsset.id == asset_id
    ).first()
    if not db_asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Актив водоснабжения не найден"
        )
    
    db.delete(db_asset)
    db.commit()
    return {"message": "Актив водоснабжения успешно удален"}


# Маршруты для обслуживания активов
@router.get("/{asset_id}/maintenance", response_model=List[AssetMaintenanceResponse])
def get_asset_maintenance_history(
    asset_id: int,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Получить историю обслуживания актива
    """
    maintenance_records = db.query(AssetMaintenance).filter(
        AssetMaintenance.asset_id == asset_id
    ).offset(skip).limit(limit).all()
    return maintenance_records


@router.post("/{asset_id}/maintenance", response_model=AssetMaintenanceResponse)
def create_asset_maintenance(
    asset_id: int,
    maintenance: AssetMaintenanceCreate, 
    db: Session = Depends(get_db)
):
    """
    Создать запись об обслуживании актива
    """
    # Проверяем, существует ли актив
    asset = db.query(WaterAsset).filter(
        WaterAsset.id == asset_id
    ).first()
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Актив водоснабжения не найден"
        )
    
    db_maintenance = AssetMaintenance(
        asset_id=asset_id,
        **maintenance.dict()
    )
    db.add(db_maintenance)
    db.commit()
    db.refresh(db_maintenance)
    return db_maintenance


@router.get("/maintenance", response_model=List[AssetMaintenanceResponse])
def get_all_maintenance_records(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получить все записи об обслуживании
    """
    maintenance_records = db.query(AssetMaintenance).offset(skip).limit(limit).all()
    return maintenance_records


@router.put("/maintenance/{maintenance_id}", response_model=AssetMaintenanceResponse)
def update_asset_maintenance(
    maintenance_id: int,
    maintenance_update: AssetMaintenanceUpdate,
    db: Session = Depends(get_db)
):
    """
    Обновить запись обслуживании актива
    """
    db_maintenance = db.query(AssetMaintenance).filter(
        AssetMaintenance.id == maintenance_id
    ).first()
    if not db_maintenance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Запись об обслуживании не найдена"
        )
    
    update_data = maintenance_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_maintenance, field, value)
    
    db.commit()
    db.refresh(db_maintenance)
    return db_maintenance


@router.get("/maintenance-due", response_model=List[WaterAssetResponse])
def get_assets_needing_maintenance(db: Session = Depends(get_db)):
    """
    Получить активы, требующие обслуживания
    """
    from datetime import datetime
    assets = db.query(WaterAsset).filter(
        WaterAsset.next_maintenance <= datetime.utcnow()
    ).all()
    return assets