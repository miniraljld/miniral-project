import apiClient from "./apiClient";
import type {
  User,
  UserLogin,
  UserLoginResponse,
  UserCreate,
  UserUpdate,
} from "./types";

const USER_API = "/users";

export const userService = {
  // Получение текущего пользователя
  getCurrentUser: async (): Promise<User> => {
    const response = await apiClient.get<User>(`${USER_API}/current`);
    return response.data;
  },

  // Получение пользователя по ID
  getUserById: async (id: number): Promise<User> => {
    const response = await apiClient.get<User>(`${USER_API}/${id}`);
    return response.data;
  },

  // Получение списка пользователей
  getUsers: async (skip: number = 0, limit: number = 100): Promise<User[]> => {
    const response = await apiClient.get<User[]>(`${USER_API}`, {
      params: { skip, limit },
    });
    return response.data;
  },

  // Создание нового пользователя
  createUser: async (userData: UserCreate): Promise<User> => {
    const response = await apiClient.post<User>(`${USER_API}`, userData);
    return response.data;
  },

  // Обновление пользователя
  updateUser: async (id: number, userData: UserUpdate): Promise<User> => {
    const response = await apiClient.put<User>(`${USER_API}/${id}`, userData);
    return response.data;
  },

  // Удаление пользователя
  deleteUser: async (id: number): Promise<void> => {
    await apiClient.delete(`${USER_API}/${id}`);
  },

  // Аутентификация пользователя
  login: async (credentials: UserLogin): Promise<UserLoginResponse> => {
    const response = await apiClient.post<UserLoginResponse>(
      `${USER_API}/token`,
      credentials
    );
    return response.data;
  },

  // Выход из системы
  logout: (): void => {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
  },
};
