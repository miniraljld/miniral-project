from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.config.database import get_db
from backend.models.notifications import Notification, NotificationSetting
from backend.schemas.notifications import (
    NotificationCreate, 
    NotificationUpdate, 
    NotificationResponse,
    NotificationSettingCreate,
    NotificationSettingUpdate,
    NotificationSettingResponse
)

router = APIRouter()

# Маршруты для уведомлений
@router.get("/", response_model=List[NotificationResponse])
def get_notifications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получить список уведомлений
    """
    notifications = db.query(Notification).offset(skip).limit(limit).all()
    return notifications


@router.get("/user", response_model=List[NotificationResponse])
def get_user_notifications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получить уведомления для текущего пользователя
    """
    # В реальном приложении здесь будет фильтрация по текущему пользователю
    notifications = db.query(Notification).offset(skip).limit(limit).all()
    return notifications


@router.post("/", response_model=NotificationResponse)
def create_notification(
    notification: NotificationCreate, 
    db: Session = Depends(get_db)
):
    """
    Создать новое уведомление
    """
    db_notification = Notification(**notification.dict())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification


@router.get("/{notification_id}", response_model=NotificationResponse)
def get_notification_by_id(
    notification_id: int, 
    db: Session = Depends(get_db)
):
    """
    Получить уведомление по ID
    """
    notification = db.query(Notification).filter(
        Notification.id == notification_id
    ).first()
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Уведомление не найдено"
        )
    return notification


@router.put("/{notification_id}", response_model=NotificationResponse)
def update_notification(
    notification_id: int,
    notification_update: NotificationUpdate,
    db: Session = Depends(get_db)
):
    """
    Обновить уведомление
    """
    db_notification = db.query(Notification).filter(
        Notification.id == notification_id
    ).first()
    if not db_notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Уведомление не найдено"
        )
    
    update_data = notification_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_notification, field, value)
    
    db.commit()
    db.refresh(db_notification)
    return db_notification


@router.delete("/{notification_id}")
def delete_notification(
    notification_id: int, 
    db: Session = Depends(get_db)
):
    """
    Удалить уведомление
    """
    db_notification = db.query(Notification).filter(
        Notification.id == notification_id
    ).first()
    if not db_notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Уведомление не найдено"
        )
    
    db.delete(db_notification)
    db.commit()
    return {"message": "Уведомление успешно удалено"}


# Маршруты для настроек уведомлений
@router.get("/settings/{user_id}", response_model=List[NotificationSettingResponse])
def get_user_notification_settings(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Получить настройки уведомлений для пользователя
    """
    settings = db.query(NotificationSetting).filter(
        NotificationSetting.user_id == user_id
    ).all()
    return settings


@router.post("/settings", response_model=NotificationSettingResponse)
def create_notification_setting(
    setting: NotificationSettingCreate, 
    db: Session = Depends(get_db)
):
    """
    Создать новые настройки уведомлений
    """
    db_setting = NotificationSetting(**setting.dict())
    db.add(db_setting)
    db.commit()
    db.refresh(db_setting)
    return db_setting


@router.put("/settings/{setting_id}", response_model=NotificationSettingResponse)
def update_notification_setting(
    setting_id: int,
    setting_update: NotificationSettingUpdate,
    db: Session = Depends(get_db)
):
    """
    Обновить настройки уведомлений
    """
    db_setting = db.query(NotificationSetting).filter(
        NotificationSetting.id == setting_id
    ).first()
    if not db_setting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Настройки уведомлений не найдены"
        )
    
    update_data = setting_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_setting, field, value)
    
    db.commit()
    db.refresh(db_setting)
    return db_setting


# Маршруты для управления уведомлениями
@router.patch("/{notification_id}/read")
def mark_notification_as_read(
    notification_id: int,
    db: Session = Depends(get_db)
):
    """
    Отметить уведомление как прочитанное
    """
    db_notification = db.query(Notification).filter(
        Notification.id == notification_id
    ).first()
    if not db_notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Уведомление не найдено"
        )
    
    db_notification.is_read = True
    db.commit()
    return {"message": "Уведомление отмечено как прочитанное"}


@router.patch("/read-all")
def mark_all_notifications_as_read(
    db: Session = Depends(get_db)
):
    """
    Отметить все уведомления как прочитанные
    """
    # В реальном приложении здесь будет фильтрация по текущему пользователю
    db.query(Notification).update({Notification.is_read: True})
    db.commit()
    return {"message": "Все уведомления отмечены как прочитанные"}