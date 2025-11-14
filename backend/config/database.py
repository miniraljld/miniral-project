from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from urllib.parse import quote_plus

# URL подключения к базе данных PostgreSQL
# postgresql://Asul_owner:npg_g2bpls0ruyVc@ep-steep-art-a8v9mw8n-pooler.eastus2.azure.neon.tech/Asul?sslmode=require
DATABASE_URL = "postgresql://Asul_owner:npg_g2bpls0ruyVc@ep-steep-art-a8v9mw8n-pooler.eastus2.azure.neon.tech/Asul?sslmode=require"

# Настройки пула подключений
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

# Создание движка базы данных с настройками пула
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,          # Количество подключений в пуле
    max_overflow=20,       # Максимальное количество дополнительных подключений
    pool_pre_ping=True,    # Проверка подключения перед использованием
    pool_recycle=300,      # Время в секундах, после которого подключение будет пересоздано
    echo=False             # Установите True для отладки SQL-запросов
)

# Кодирование пароля для корректной обработки специальных символов в URL
# encoded_password = quote_plus("npg_g2bpls0ruyVc")
# DATABASE_URL = f"postgresql://Asul_owner:{encoded_password}@ep-steep-art-a8v9mw8n-pooler.eastus2.azure.neon.tech/Asul?sslmode=require"

# Создание движка базы данных
engine = create_engine(DATABASE_URL)

# Создание локальной сессии
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

# Функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()