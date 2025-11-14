import apiClient from "./apiClient";
import type { Notification, NotificationSetting } from "./types";

const NOTIFICATIONS_API = "/notifications";

export const notificationsService = {
  // Получение всех уведомлений для текущего пользователя
  getUserNotifications: async (
    skip: number = 0,
    limit: number = 100
  ): Promise<Notification[]> => {
    const response = await apiClient.get<Notification[]>(
      `${NOTIFICATIONS_API}/user`,
      {
        params: { skip, limit },
      }
    );
    return response.data;
  },

  // Получение уведомления по ID
  getNotificationById: async (id: number): Promise<Notification> => {
    const response = await apiClient.get<Notification>(
      `${NOTIFICATIONS_API}/${id}`
    );
    return response.data;
  },

  // Создание нового уведомления
  createNotification: async (
    notificationData: Omit<Notification, "id" | "created_at" | "updated_at">
  ): Promise<Notification> => {
    const response = await apiClient.post<Notification>(
      NOTIFICATIONS_API,
      notificationData
    );
    return response.data;
  },

  // Обновление уведомления
  updateNotification: async (
    id: number,
    notificationData: Partial<Notification>
  ): Promise<Notification> => {
    const response = await apiClient.put<Notification>(
      `${NOTIFICATIONS_API}/${id}`,
      notificationData
    );
    return response.data;
  },

  // Удаление уведомления
  deleteNotification: async (id: number): Promise<void> => {
    await apiClient.delete(`${NOTIFICATIONS_API}/${id}`);
  },

  // Отметка уведомления как прочитанного
  markAsRead: async (id: number): Promise<Notification> => {
    const response = await apiClient.patch<Notification>(
      `${NOTIFICATIONS_API}/${id}/read`
    );
    return response.data;
  },

  // Отметка всех уведомлений как прочитанных
  markAllAsRead: async (): Promise<void> => {
    await apiClient.patch(`${NOTIFICATIONS_API}/read-all`);
  },

  // Получение настроек уведомлений для пользователя
  getUserNotificationSettings: async (
    userId: number
  ): Promise<NotificationSetting[]> => {
    const response = await apiClient.get<NotificationSetting[]>(
      `${NOTIFICATIONS_API}/settings/${userId}`
    );
    return response.data;
  },

  // Обновление настроек уведомлений для пользователя
  updateNotificationSettings: async (
    userId: number,
    settings: Partial<NotificationSetting>[]
  ): Promise<NotificationSetting[]> => {
    const response = await apiClient.put<NotificationSetting[]>(
      `${NOTIFICATIONS_API}/settings/${userId}`,
      settings
    );
    return response.data;
  },

  // Создание новых настроек уведомлений для пользователя
  createNotificationSettings: async (
    settingsData: Omit<NotificationSetting, "id" | "created_at" | "updated_at">
  ): Promise<NotificationSetting> => {
    const response = await apiClient.post<NotificationSetting>(
      `${NOTIFICATIONS_API}/settings`,
      settingsData
    );
    return response.data;
  },
};
