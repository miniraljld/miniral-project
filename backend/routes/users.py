from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta

from backend.config.database import get_db
from backend.models.user import User, UserRole
from backend.schemas.user import UserCreate, UserUpdate, UserResponse
from backend.utils.auth import get_password_hash, authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_active_user
from backend.utils.role_checker import require_admin, require_delete_user, require_edit_user

router = APIRouter()

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Создание нового пользователя
    """
    # Проверяем, существует ли уже пользователь с таким именем или email
    existing_user_by_username = db.query(User).filter(User.username == user.username).first()
    existing_user_by_email = db.query(User).filter(User.email == user.email).first()
    
    if existing_user_by_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким именем уже существует"
        )
    
    if existing_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует"
        )
    
    # Создаем нового пользователя с ролью USER по умолчанию
    db_user = User(
        username=user.username,
        email=user.email,  # email может быть None
        full_name=user.full_name,
        hashed_password=get_password_hash(user.password),
        is_active=user.is_active,
        role=UserRole.USER  # Все новые пользователи получают роль USER по умолчанию
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    # Проверяем права доступа к просмотру информации пользователя
    if current_user.role != UserRole.ADMIN and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для просмотра информации другого пользователя"
        )
    
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    return db_user
    """
    Получение пользователя по ID
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    return db_user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, current_user: User = Depends(require_edit_user), db: Session = Depends(get_db)):
    """
    Обновление пользователя по ID
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    
    # Обновляем поля пользователя
    update_data = user.dict(exclude_unset=True)
    if "password" in update_data and update_data["password"]:
        update_data["hashed_password"] = get_password_hash(update_data["password"])
        del update_data["password"]
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    
    return db_user


@router.delete("/{user_id}")
def delete_user(user_id: int, current_user: User = Depends(require_delete_user), db: Session = Depends(get_db)):
    """
    Удаление пользователя по ID
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    
    db.delete(db_user)
    db.commit()
    
    return {"message": "Пользователь успешно удален"}


@router.get("/", response_model=List[UserResponse])
def get_users(skip: int = 0, limit: int = 100, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    """
    Получение списка пользователей с пагинацией
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users


from pydantic import BaseModel

class UserLogin(BaseModel):
    username: str
    password: str

@router.post("/token")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Аутентификация пользователя и получение токена
    """
    user = authenticate_user(db, credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username
    }