from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.config.database import get_db
from backend.models.complaints import Complaint, ComplaintCategory
from backend.schemas.complaints import (
    ComplaintCreate, 
    ComplaintUpdate, 
    ComplaintResponse,
    ComplaintCategoryCreate,
    ComplaintCategoryUpdate,
    ComplaintCategoryResponse
)

router = APIRouter()

@router.get("/", response_model=List[ComplaintResponse])
def get_complaints(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получить список жалоб
    """
    complaints = db.query(Complaint).offset(skip).limit(limit).all()
    return complaints


@router.post("/", response_model=ComplaintResponse)
def create_complaint(
    complaint: ComplaintCreate, 
    db: Session = Depends(get_db)
):
    """
    Создать новую жалобу
    """
    db_complaint = Complaint(**complaint.dict())
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    return db_complaint


@router.get("/{complaint_id}", response_model=ComplaintResponse)
def get_complaint_by_id(
    complaint_id: int, 
    db: Session = Depends(get_db)
):
    """
    Получить жалобу по ID
    """
    complaint = db.query(Complaint).filter(
        Complaint.id == complaint_id
    ).first()
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Жалоба не найдена"
        )
    return complaint


@router.put("/{complaint_id}", response_model=ComplaintResponse)
def update_complaint(
    complaint_id: int,
    complaint_update: ComplaintUpdate,
    db: Session = Depends(get_db)
):
    """
    Обновить жалобу
    """
    db_complaint = db.query(Complaint).filter(
        Complaint.id == complaint_id
    ).first()
    if not db_complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Жалоба не найдена"
        )
    
    update_data = complaint_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_complaint, field, value)
    
    db.commit()
    db.refresh(db_complaint)
    return db_complaint


@router.delete("/{complaint_id}")
def delete_complaint(
    complaint_id: int, 
    db: Session = Depends(get_db)
):
    """
    Удалить жалобу
    """
    db_complaint = db.query(Complaint).filter(
        Complaint.id == complaint_id
    ).first()
    if not db_complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Жалоба не найдена"
        )
    
    db.delete(db_complaint)
    db.commit()
    return {"message": "Жалоба успешно удалена"}


# Маршруты для категорий жалоб
@router.get("/categories", response_model=List[ComplaintCategoryResponse])
def get_complaint_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получить список категорий жалоб
    """
    categories = db.query(ComplaintCategory).offset(skip).limit(limit).all()
    return categories


@router.post("/categories", response_model=ComplaintCategoryResponse)
def create_complaint_category(
    category: ComplaintCategoryCreate, 
    db: Session = Depends(get_db)
):
    """
    Создать новую категорию жалоб
    """
    db_category = ComplaintCategory(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@router.get("/categories/{category_id}", response_model=ComplaintCategoryResponse)
def get_complaint_category_by_id(
    category_id: int, 
    db: Session = Depends(get_db)
):
    """
    Получить категорию жалоб по ID
    """
    category = db.query(ComplaintCategory).filter(
        ComplaintCategory.id == category_id
    ).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория жалоб не найдена"
        )
    return category


@router.put("/categories/{category_id}", response_model=ComplaintCategoryResponse)
def update_complaint_category(
    category_id: int,
    category_update: ComplaintCategoryUpdate,
    db: Session = Depends(get_db)
):
    """
    Обновить категорию жалоб
    """
    db_category = db.query(ComplaintCategory).filter(
        ComplaintCategory.id == category_id
    ).first()
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория жалоб не найдена"
        )
    
    update_data = category_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_category, field, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category


@router.patch("/{complaint_id}/assign")
def assign_complaint(
    complaint_id: int,
    assigned_to: int,
    db: Session = Depends(get_db)
):
    """
    Назначить жалобу на исполнение
    """
    db_complaint = db.query(Complaint).filter(
        Complaint.id == complaint_id
    ).first()
    if not db_complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Жалоба не найдена"
        )
    
    db_complaint.assigned_to = assigned_to
    db.commit()
    return {"message": "Жалоба назначена на исполнение"}


@router.patch("/{complaint_id}/resolve")
def resolve_complaint(
    complaint_id: int,
    db: Session = Depends(get_db)
):
    """
    Отметить жалобу как решенную
    """
    db_complaint = db.query(Complaint).filter(
        Complaint.id == complaint_id
    ).first()
    if not db_complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Жалоба не найдена"
        )
    
    db_complaint.status = "resolved"
    db_complaint.resolved_at = db.func.now()
    db.commit()
    return {"message": "Жалоба отмечена как решенная"}