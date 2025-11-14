import React, { useEffect, useState, useCallback } from "react";
import { notificationsService } from "../api/notificationsService";
import type { Notification } from "../api/types";

const NotificationPanel: React.FC = () => {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [updatingId, setUpdatingId] = useState<number | null>(null);

  const loadNotifications = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await notificationsService.getUserNotifications(0, 50);
      setNotifications(data);
    } catch (err) {
      console.error("Ошибка загрузки уведомлений:", err);
      setError("Не удалось загрузить уведомления. Проверьте API.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadNotifications();
  }, [loadNotifications]);

  const getNotificationTypeColor = (type: string) => {
    switch (type) {
      case "info":
        return "#2196F3";
      case "warning":
        return "#FFC107";
      case "alert":
        return "#F44336";
      default:
        return "#9E9E9E";
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case "low":
        return "#4CAF50";
      case "medium":
        return "#FFC107";
      case "high":
        return "#F44336";
      default:
        return "#9E9E9E";
    }
  };

  const markAsRead = async (id: number) => {
    setUpdatingId(id);
    try {
      await notificationsService.markAsRead(id);
      setNotifications((prev) =>
        prev.map((notification) =>
          notification.id === id
            ? { ...notification, is_read: true }
            : notification
        )
      );
    } catch (err) {
      console.error("Ошибка обновления уведомления:", err);
      setError("Не удалось обновить уведомление.");
    } finally {
      setUpdatingId(null);
    }
  };

  const renderContent = () => {
    if (loading) {
      return <p>Загрузка уведомлений...</p>;
    }

    if (error) {
      return (
        <div className="error-state">
          <p>{error}</p>
          <button className="refresh-btn" onClick={loadNotifications}>
            Повторить
          </button>
        </div>
      );
    }

    if (notifications.length === 0) {
      return <p>Уведомления отсутствуют.</p>;
    }

    return (
      <div className="notifications-list">
        {notifications.map((notification) => (
          <div
            key={notification.id}
            className={`notification-item ${
              !notification.is_read ? "unread" : ""
            }`}
          >
            <div className="notification-header">
              <div
                className="notification-type"
                style={{
                  backgroundColor: getNotificationTypeColor(
                    notification.notification_type
                  ),
                }}
              >
                {notification.notification_type === "info"
                  ? "И"
                  : notification.notification_type === "warning"
                  ? "П"
                  : "Т"}
              </div>
              <div className="notification-title">
                <h4>{notification.title}</h4>
                <span className="notification-date">
                  {new Date(notification.created_at).toLocaleString()}
                </span>
              </div>
              <div
                className="notification-priority"
                style={{
                  backgroundColor: getPriorityColor(notification.priority),
                }}
              >
                {notification.priority === "low"
                  ? "Н"
                  : notification.priority === "medium"
                  ? "С"
                  : "В"}
              </div>
            </div>
            <div className="notification-content">
              <p>{notification.message}</p>
            </div>
            <div className="notification-actions">
              {!notification.is_read && (
                <button
                  className="action-btn mark-read-btn"
                  onClick={() => markAsRead(notification.id)}
                  disabled={updatingId === notification.id}
                >
                  {updatingId === notification.id
                    ? "Обновление..."
                    : "Отметить как прочитанное"}
                </button>
              )}
              <button className="action-btn view-btn">Подробнее</button>
            </div>
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="notification-panel">
      <div className="panel-controls">
        <select className="filter-select">
          <option value="all">Все типы</option>
          <option value="info">Информационные</option>
          <option value="warning">Предупреждения</option>
          <option value="alert">Тревоги</option>
        </select>
        <select className="filter-select">
          <option value="all">Все приоритеты</option>
          <option value="low">Низкий</option>
          <option value="medium">Средний</option>
          <option value="high">Высокий</option>
        </select>
        <select className="filter-select">
          <option value="all">Все статусы</option>
          <option value="unread">Непрочитанные</option>
          <option value="read">Прочитанные</option>
        </select>
        <button className="refresh-btn" onClick={loadNotifications}>
          Обновить
        </button>
        <button className="add-btn">Создать уведомление</button>
      </div>

      {renderContent()}
    </div>
  );
};

export { NotificationPanel };
