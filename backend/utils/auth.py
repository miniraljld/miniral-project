from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
import os

from backend.config.database import get_db
from backend.models.user import User

# Ключ для подписи JWT токенов (в реальном приложении нужно хранить в переменных окружения)
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Для хеширования паролей
pwd_context = CryptContext(schemes=["plaintext"], deprecated="auto")

# Для OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    """
    Проверяет, соответствует ли введенный пароль хешированному паролю
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    Возвращает хеш для переданного пароля
    """
    # Ограничиваем длину пароля до 72 байт, как того требует bcrypt
    truncated_password = password[:72] if len(password) > 72 else password
    # Проверяем, что пароль не пустой после обрезки
    if not truncated_password:
        raise ValueError("Пароль не может быть пустым")
    return pwd_context.hash(truncated_password)

def authenticate_user(db: Session, username: str, password: str):
    """
    Аутентифицирует пользователя по имени и паролю
    """
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Создает JWT токен с указанными данными
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Возвращает текущего пользователя на основе токена
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
    Возвращает текущего активного пользователя
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user