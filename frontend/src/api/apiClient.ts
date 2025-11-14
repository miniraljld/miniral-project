import axios from "axios";

// Базовая конфигурация API
const API_BASE_URL =
  import.meta.env.VITE_API_URL || "http://localhost:8000/api";

// Создание экземпляра axios с базовыми настройками
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000, // Таймаут 10 секунд
  headers: {
    "Content-Type": "application/json",
  },
});

// Перехватчик запросов для добавления токена аутентификации
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Перехватчик ответов для обработки ошибок
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Токен истек или недействителен - очищаем данные аутентификации
      localStorage.removeItem("token");
      localStorage.removeItem("username");
      // Можно добавить перенаправление на страницу входа
    }
    return Promise.reject(error);
  }
);

export default apiClient;
