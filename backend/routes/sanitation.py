from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.config.database import get_db
from backend.models.sanitation import SanitationFacility, SanitationReport
from backend.schemas.sanitation import (
    SanitationFacilityCreate, 
    SanitationFacilityUpdate, 
    SanitationFacilityResponse,
    SanitationReportCreate,
    SanitationReportUpdate,
    SanitationReportResponse
)

router = APIRouter()

@router.get("/", response_model=List[SanitationFacilityResponse])
def get_sanitation_facilities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получить список санитарных сооружений
    """
    facilities = db.query(SanitationFacility).offset(skip).limit(limit).all()
    return facilities


@router.post("/", response_model=SanitationFacilityResponse)
def create_sanitation_facility(
    facility: SanitationFacilityCreate, 
    db: Session = Depends(get_db)
):
    """
    Создать новое санитарное сооружение
    """
    db_facility = SanitationFacility(**facility.dict())
    db.add(db_facility)
    db.commit()
    db.refresh(db_facility)
    return db_facility


@router.get("/{facility_id}", response_model=SanitationFacilityResponse)
def get_sanitation_facility_by_id(
    facility_id: int, 
    db: Session = Depends(get_db)
):
    """
    Получить санитарное сооружение по ID
    """
    facility = db.query(SanitationFacility).filter(
        SanitationFacility.id == facility_id
    ).first()
    if not facility:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Санитарное сооружение не найдено"
        )
    return facility


@router.put("/{facility_id}", response_model=SanitationFacilityResponse)
def update_sanitation_facility(
    facility_id: int,
    facility_update: SanitationFacilityUpdate,
    db: Session = Depends(get_db)
):
    """
    Обновить санитарное сооружение
    """
    db_facility = db.query(SanitationFacility).filter(
        SanitationFacility.id == facility_id
    ).first()
    if not db_facility:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Санитарное сооружение не найдено"
        )
    
    update_data = facility_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_facility, field, value)
    
    db.commit()
    db.refresh(db_facility)
    return db_facility


@router.delete("/{facility_id}")
def delete_sanitation_facility(
    facility_id: int, 
    db: Session = Depends(get_db)
):
    """
    Удалить санитарное сооружение
    """
    db_facility = db.query(SanitationFacility).filter(
        SanitationFacility.id == facility_id
    ).first()
    if not db_facility:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Санитарное сооружение не найдено"
        )
    
    db.delete(db_facility)
    db.commit()
    return {"message": "Санитарное сооружение успешно удалено"}


# Маршруты для отчетов о санитарии
@router.get("/reports", response_model=List[SanitationReportResponse])
def get_sanitation_reports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получить список отчетов о санитарии
    """
    reports = db.query(SanitationReport).offset(skip).limit(limit).all()
    return reports


@router.post("/reports", response_model=SanitationReportResponse)
def create_sanitation_report(
    report: SanitationReportCreate, 
    db: Session = Depends(get_db)
):
    """
    Создать новый отчет о санитарии
    """
    db_report = SanitationReport(**report.dict())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report


@router.get("/reports/{report_id}", response_model=SanitationReportResponse)
def get_sanitation_report_by_id(
    report_id: int, 
    db: Session = Depends(get_db)
):
    """
    Получить отчет о санитарии по ID
    """
    report = db.query(SanitationReport).filter(
        SanitationReport.id == report_id
    ).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Отчет о санитарии не найден"
        )
    return report


@router.put("/reports/{report_id}", response_model=SanitationReportResponse)
def update_sanitation_report(
    report_id: int,
    report_update: SanitationReportUpdate,
    db: Session = Depends(get_db)
):
    """
    Обновить отчет о санитарии
    """
    db_report = db.query(SanitationReport).filter(
        SanitationReport.id == report_id
    ).first()
    if not db_report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Отчет о санитарии не найден"
        )
    
    update_data = report_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_report, field, value)
    
    db.commit()
    db.refresh(db_report)
    return db_report