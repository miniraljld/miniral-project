#!/usr/bin/env python3
"""
Скрипт для создания администратора в базе данных
"""
import os
import sys
from getpass import getpass

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from backend.config.database import SessionLocal, engine
from backend.models.user import User, UserRole
from backend.utils.auth import get_password_hash


def create_admin_user():
    """
    Создает администратора в базе данных
    """
    print("Создание администратора в базе данных...")
    
    # Получаем данные от пользователя
    username = input("Введите имя пользователя для администратора: ").strip()
    if not username:
        print("Имя пользователя не может быть пустым")
        return False
    
    email = input("Введите email для администратора: ").strip()
    if not email:
        print("Email не может быть пустым")
        return False
    
    full_name = input("Введите полное имя администратора (необязательно): ").strip()
    
    password = getpass("Введите пароль для администратора: ")
    if not password:
        print("Пароль не может быть пустым")
        return False
    
    confirm_password = getpass("Подтвердите пароль: ")
    if password != confirm_password:
        print("Пароли не совпадают")
        return False
    
    # Создаем сессию базы данных
    db: Session = SessionLocal()
    
    try:
        # Проверяем, существует ли уже пользователь с таким именем
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            print(f"Пользователь с именем '{username}' уже существует")
            return False
        
        # Проверяем, существует ли уже пользователь с таким email
        existing_email = db.query(User).filter(User.email == email).first()
        if existing_email:
            print(f"Пользователь с email '{email}' уже существует")
            return False
        
        # Создаем нового администратора
        hashed_password = get_password_hash(password)
        admin_user = User(
            username=username,
            email=email,
            full_name=full_name if full_name else username,
            hashed_password=hashed_password,
            is_active=True,
            role=UserRole.ADMIN
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