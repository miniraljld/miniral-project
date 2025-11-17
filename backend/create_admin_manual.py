#!/usr/bin/env python3
"""
Скрипт для ручного создания администратора в базе данных с фиксированными учетными данными
"""
import os
import sys

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from backend.config.database import SessionLocal, engine
from backend.models.user import User, UserRole
from backend.utils.auth import get_password_hash

def create_admin_user():
    """
    Создает администратора в базе данных с фиксированными учетными данными
    """
    print("Создание администратора в базе данных...")
    
    # Учетные данные администратора
    username = "admin"
    password = "admin0772"
    email = "admin@example.com"
    full_name = "Administrator"
    
    # Создаем сессию базы данных
    db: Session = SessionLocal()
    
    try:
        # Проверяем, существует ли уже пользователь с таким именем
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            print(f"Пользователь с именем '{username}' уже существует")
            print(f"Обновляем роль пользователя на ADMIN")
            existing_user.role = UserRole.ADMIN
            db.commit()
            print(f"Роль пользователя '{username}' обновлена до ADMIN")
            return True
        
        # Создаем нового администратора
        hashed_password = get_password_hash(password)
        admin_user = User(
            username=username,
            email=email,
            full_name=full_name,
            hashed_password=hashed_password,
            is_active=True,
            role=UserRole.ADMIN  # Убедимся, что роль устанавливается как ADMIN
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print(f"Администратор '{username}' успешно создан с ID {admin_user.id}")
        return True
        
    except Exception as e:
        print(f"Ошибка при создании администратора: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = create_admin_user()
    if success:
        print("Процесс завершен успешно")
        sys.exit(0)
    else:
        print("Процесс завершен с ошибкой")
        sys.exit(1)