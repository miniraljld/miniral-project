from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.config.database import get_db
from backend.models.tariffs import Tariff, PaymentMethod, UserPayment
from backend.schemas.tariffs import (
    TariffCreate, 
    TariffUpdate, 
    TariffResponse,
    PaymentMethodCreate,
    PaymentMethodUpdate,
    PaymentMethodResponse,
    UserPaymentCreate,
    UserPaymentUpdate,
    UserPaymentResponse
)

router = APIRouter()

# Маршруты для тарифов
@router.get("/", response_model=List[TariffResponse])
def get_tariffs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получить список тарифов
    """
    tariffs = db.query(Tariff).offset(skip).limit(limit).all()
    return tariffs


@router.post("/", response_model=TariffResponse)
def create_tariff(
    tariff: TariffCreate, 
    db: Session = Depends(get_db)
):
    """
    Создать новый тариф
    """
    db_tariff = Tariff(**tariff.dict())
    db.add(db_tariff)
    db.commit()
    db.refresh(db_tariff)
    return db_tariff


@router.get("/{tariff_id}", response_model=TariffResponse)
def get_tariff_by_id(
    tariff_id: int, 
    db: Session = Depends(get_db)
):
    """
    Получить тариф по ID
    """
    tariff = db.query(Tariff).filter(
        Tariff.id == tariff_id
    ).first()
    if not tariff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тариф не найден"
        )
    return tariff


@router.put("/{tariff_id}", response_model=TariffResponse)
def update_tariff(
    tariff_id: int,
    tariff_update: TariffUpdate,
    db: Session = Depends(get_db)
):
    """
    Обновить тариф
    """
    db_tariff = db.query(Tariff).filter(
        Tariff.id == tariff_id
    ).first()
    if not db_tariff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тариф не найден"
        )
    
    update_data = tariff_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_tariff, field, value)
    
    db.commit()
    db.refresh(db_tariff)
    return db_tariff


@router.delete("/{tariff_id}")
def delete_tariff(
    tariff_id: int, 
    db: Session = Depends(get_db)
):
    """
    Удалить тариф
    """
    db_tariff = db.query(Tariff).filter(
        Tariff.id == tariff_id
    ).first()
    if not db_tariff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тариф не найден"
        )
    
    db.delete(db_tariff)
    db.commit()
    return {"message": "Тариф успешно удален"}


# Маршруты для способов оплаты
@router.get("/payment-methods", response_model=List[PaymentMethodResponse])
def get_payment_methods(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получить список способов оплаты
    """
    methods = db.query(PaymentMethod).offset(skip).limit(limit).all()
    return methods


@router.post("/payment-methods", response_model=PaymentMethodResponse)
def create_payment_method(
    method: PaymentMethodCreate, 
    db: Session = Depends(get_db)
):
    """
    Создать новый способ оплаты
    """
    db_method = PaymentMethod(**method.dict())
    db.add(db_method)
    db.commit()
    db.refresh(db_method)
    return db_method


@router.get("/payment-methods/{method_id}", response_model=PaymentMethodResponse)
def get_payment_method_by_id(
    method_id: int, 
    db: Session = Depends(get_db)
):
    """
    Получить способ оплаты по ID
    """
    method = db.query(PaymentMethod).filter(
        PaymentMethod.id == method_id
    ).first()
    if not method:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Способ оплаты не найден"
        )
    return method


@router.put("/payment-methods/{method_id}", response_model=PaymentMethodResponse)
def update_payment_method(
    method_id: int,
    method_update: PaymentMethodUpdate,
    db: Session = Depends(get_db)
):
    """
    Обновить способ оплаты
    """
    db_method = db.query(PaymentMethod).filter(
        PaymentMethod.id == method_id
    ).first()
    if not db_method:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Способ оплаты не найден"
        )
    
    update_data = method_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_method, field, value)
    
    db.commit()
    db.refresh(db_method)
    return db_method


# Маршруты для платежей пользователей
@router.get("/payments", response_model=List[UserPaymentResponse])
def get_user_payments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получить список платежей пользователей
    """
    payments = db.query(UserPayment).offset(skip).limit(limit).all()
    return payments


@router.post("/payments", response_model=UserPaymentResponse)
def create_user_payment(
    payment: UserPaymentCreate, 
    db: Session = Depends(get_db)
):
    """
    Создать новый платеж пользователя
    """
    db_payment = UserPayment(**payment.dict())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment


@router.get("/payments/{payment_id}", response_model=UserPaymentResponse)
def get_user_payment_by_id(
    payment_id: int, 
    db: Session = Depends(get_db)
):
    """
    Получить платеж пользователя по ID
    """
    payment = db.query(UserPayment).filter(
        UserPayment.id == payment_id
    ).first()
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Платеж не найден"
        )
    return payment