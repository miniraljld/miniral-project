"""
Модуль содержит маршруты для системы мониторинга и управления водоснабжением
"""
from .users import router as users
from .water_infrastructure import router as water_infrastructure
from .water_quality import router as water_quality
from .sanitation import router as sanitation
from .complaints import router as complaints
from .tariffs import router as tariffs
from .assets import router as assets
from .demand_forecasting import router as demand_forecasting
from .notifications import router as notifications