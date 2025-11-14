from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from backend.config.database import engine, Base
from backend.config.settings import APP_NAME, APP_DESCRIPTION, APP_VERSION, ALLOWED_ORIGINS
from backend.routes import (
    users,
    water_infrastructure,
    water_quality,
    sanitation,
    complaints,
    tariffs,
    assets,
    demand_forecasting,
    notifications
)
from backend.utils.auth import oauth2_scheme

# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)

# Инициализация FastAPI приложения
app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION
)

# Настройка CORS

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origin_regex=None,
    expose_headers=["Access-Control-Allow-Origin"]
)

# Подключение маршрутов
app.include_router(users, prefix="/api/users", tags=["Пользователи"])
app.include_router(water_infrastructure, prefix="/api/water-infrastructure", tags=["Инфраструктура водоснабжения"])
app.include_router(water_quality, prefix="/api/water-quality", tags=["Качество воды"])
app.include_router(sanitation, prefix="/api/sanitation", tags=["Санитария"])
app.include_router(complaints, prefix="/api/complaints", tags=["Жалобы"])
app.include_router(tariffs, prefix="/api/tariffs", tags=["Тарифы"])
app.include_router(assets, prefix="/api/assets", tags=["Активы"])
app.include_router(demand_forecasting, prefix="/api/demand", tags=["Спрос и планирование"])
app.include_router(notifications, prefix="/api/notifications", tags=["Уведомления"])

# Корневой маршрут
@app.get("/")
def read_root():
    return {
        "message": "Добро пожаловать в API веб-платформы мониторинга и управления системами водоснабжения!",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Маршрут для проверки аутентификации
@app.get("/api/protected")
def protected_route(token: str = Depends(oauth2_scheme)):
    return {"message": "Этот маршрут защищен JWT токеном", "token": token}