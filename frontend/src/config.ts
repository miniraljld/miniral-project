// Конфигурационный файл для фронтенда

// Базовый URL для API
export const API_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_URL || "http://localhost:8000/api",
  TIMEOUT: 30000, // 30 секунд таймаута
};

// Конфигурация для карты (например, Leaflet или Google Maps)
export const MAP_CONFIG = {
  DEFAULT_CENTER: [42.8747, 74.61], // Координаты Бишкека по умолчанию
  DEFAULT_ZOOM: 13,
  TILE_LAYER: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
  TILE_LAYER_ATTRIBUTION:
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
};

// Конфигурация приложения
export const APP_CONFIG = {
  NAME: "Веб-платформа мониторинга и управления системами водоснабжения",
  VERSION: "1.0.0",
  DESCRIPTION:
    "Платформа для хакатона «От источника к решению: цифровой путь к воде»",
  DEFAULT_LANGUAGE: "ru",
};

// Настройки для уведомлений
export const NOTIFICATION_CONFIG = {
  DURATION: 5000, // 5 секунд для отображения уведомлений
  POSITION: "top-right" as const,
};

// Настройки для аутентификации
export const AUTH_CONFIG = {
  TOKEN_KEY: "token",
  REFRESH_TOKEN_KEY: "refresh_token",
  USER_KEY: "user",
  SESSION_TIMEOUT: 30 * 60 * 1000, // 30 минут
};
