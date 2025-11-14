from typing import Callable, List
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.models.user import User, UserRole
from backend.utils.auth import get_current_active_user


def check_role(required_roles: List[UserRole]) -> Callable:
    """
    Декоратор для проверки роли пользователя
    """
    async def role_checker(
        current_user: User = Depends(get_current_active_user)
    ) -> User:
        if current_user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для выполнения этого действия"
            )
        return current_user
    
    return role_checker


# Проверка прав для обычного пользователя
def require_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    if current_user.role not in [UserRole.USER, UserRole.ENGINEER, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для выполнения этого действия"
        )
    return current_user


# Проверка прав для инженера
def require_engineer(
    current_user: User = Depends(get_current_active_user)
) -> User:
    if current_user.role not in [UserRole.ENGINEER, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для выполнения этого действия"
        )
    return current_user


# Проверка прав для администратора
def require_admin(
    current_user: User = Depends(get_current_active_user)
) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для выполнения этого действия"
        )
    return current_user


# Проверка прав для редактирования данных пользователя
def require_edit_user(
    user_id: int,
    current_user: User = Depends(get_current_active_user)
) -> User:
    if current_user.role == UserRole.ADMIN:
        return current_user
    elif current_user.role == UserRole.ENGINEER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Инженеры не могут редактировать пользователей"
        )
    elif current_user.id == user_id:
        return current_user
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для редактирования этого пользователя"
        )


# Проверка прав для удаления пользователя
def require_delete_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только администраторы могут удалять пользователей"
        )
    return current_user