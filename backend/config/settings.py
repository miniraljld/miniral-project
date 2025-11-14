"""
Файл конфигурации для бэкенда
"""
import os
from typing import List

# Настройки базы данных
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://Asul_owner:npg_g2bpls0ruyVc@ep-steep-art-a8v9mw8n-pooler.eastus2.azure.neon.tech/Asul?sslmode=require"
)

# Настройки JWT
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Настройки CORS
ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vite default port
    "http://localhost:3000",  # React default port
    "http://localhost:8000",  # Backend port
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    # В продакшене добавьте сюда домен вашего фронтенда
]

# Настройки приложения
APP_NAME = "Веб-платформа мониторинга и управления системами водоснабжения"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Платформа для хакатона «От источника к решению: цифровой путь к воде»"

# Настройки логирования
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Настройки безопасности
MAX_LOGIN_ATTEMPTS = 5
LOGIN_ATTEMPT_WINDOW = 900  # 15 минут в секундах

# Настройки пагинации
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Настройки кэширования (если будет использоваться)
CACHE_TTL = 300  # 5 минут в секундах