#!/usr/bin/env python3
"""
Скрипт для исправления недопустимых значений ролей пользователей в базе данных
"""
import os
import sys

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from backend.config.database import engine

def fix_user_roles():
    """
    Исправляет недопустимые значения ролей пользователей с помощью прямого SQL
    """
    print("Исправление недопустимых значений ролей пользователей...")
    
    try:
        # Подключаемся к базе данных
        with engine.connect() as connection:
            # Начинаем транзакцию
            with connection.begin():
                # Находим все недопустимые значения ролей и меняем их на 'USER'
                # Предполагаем, что возможные недопустимые значения могут быть: 'citizen', и т.д.
                invalid_roles = ['citizen', 'moderator', 'adminstrator', 'engineer_user', '']  # список потенциальных недопустимых значений
                
                for invalid_role in invalid_roles:
                    # Подсчитываем количество пользователей с недопустимой ролью
                    count_query = text("SELECT COUNT(*) FROM users WHERE role = :role")
                    result = connection.execute(count_query, {"role": invalid_role})
                    count = result.scalar()
                    
                    if count > 0:
                        print(f"Найдено {count} пользователей с недопустимой ролью '{invalid_role}'")
                        
                        # Обновляем недопустимые роли на 'USER'
                        update_query = text("UPDATE users SET role = 'USER' WHERE role = :role")
                        connection.execute(update_query, {"role": invalid_role})
                        print(f"  Роль '{invalid_role}' исправлена на 'USER'")
                
                # Также можем исправить любые другие значения, которые не входят в допустимый список
                # Обновляем все, что не входит в допустимые значения, на 'USER'
                update_query = text("""
                    UPDATE users
                    SET role = 'USER'
                    WHERE role NOT IN ('USER', 'ENGINEER', 'ADMIN')
                """)
                result = connection.execute(update_query)
                if result.rowcount > 0:
                    print(f"  Исправлено {result.rowcount} пользователей с недопустимыми ролями")
                
        print("Все недопустимые роли были исправлены")
        
    except Exception as e:
        print(f"Ошибка при исправлении ролей: {e}")

if __name__ == "__main__":
    fix_user_roles()