import React, { useEffect, useState, useCallback } from "react";
import { complaintsService } from "../api/complaintsService";
import type { Complaint } from "../api/types";

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

const getStatusColor = (status: string) => {
  switch (status) {
    case "open":
      return "#F44336";
    case "in_progress":
      return "#FFC107";
    case "resolved":
      return "#4CAF50";
    default:
      return "#9E9E9E";
  }
};

const ComplaintsList: React.FC = () => {
  const [complaints, setComplaints] = useState<Complaint[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadComplaints = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await complaintsService.getAllComplaints(0, 50);
      setComplaints(data);
    } catch (err) {
      console.error("Ошибка загрузки жалоб:", err);
      setError("Не удалось загрузить жалобы. Проверьте подключение к API.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadComplaints();
  }, [loadComplaints]);

  const formatDate = (date?: string) => {
    if (!date) return "—";
    return new Date(date).toLocaleDateString();
  };

  const renderContent = () => {
    if (loading) {
      return <p>Загрузка жалоб...</p>;
    }

    if (error) {
      return (
        <div className="error-state">
          <p>{error}</p>
          <button className="refresh-btn" onClick={loadComplaints}>
            Повторить
          </button>
        </div>
      );
    }

    if (complaints.length === 0) {
      return <p>Жалобы отсутствуют. Добавьте данные через backend API.</p>;
    }

    return (
      <div className="complaints-table">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Имя</th>
              <th>Категория</th>
              <th>Местоположение</th>
              <th>Описание</th>
              <th>Приоритет</th>
              <th>Статус</th>
              <th>Дата</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            {complaints.map((complaint) => (
              <tr key={complaint.id}>
                <td>{complaint.id}</td>
                <td>{complaint.full_name || "Аноним"}</td>
                <td>{complaint.category}</td>
                <td>{complaint.location || "Не указано"}</td>
                <td>
                  {complaint.description?.substring(0, 50)}
                  {complaint.description && complaint.description.length > 50
                    ? "..."
                    : ""}
                </td>
                <td>
                  <span
                    className="priority-indicator"
                    style={{
                      backgroundColor: getPriorityColor(complaint.priority),
                    }}
                  >
                    {complaint.priority === "low"
                      ? "Низкий"
                      : complaint.priority === "medium"
                      ? "Средний"
                      : complaint.priority === "high"
                      ? "Высокий"
                      : "Не указано"}
                  </span>
                </td>
                <td>
                  <span
                    className="status-indicator"
                    style={{
                      backgroundColor: getStatusColor(complaint.status),
                    }}
                  >
                    {complaint.status === "open"
                      ? "Открыта"
                      : complaint.status === "in_progress"
                      ? "В процессе"
                      : complaint.status === "resolved"
                      ? "Решена"
                      : "Неизвестно"}
                  </span>
                </td>
                <td>{formatDate(complaint.created_at)}</td>
                <td>
                  <button className="action-btn view-btn">Просмотр</button>
                  <button className="action-btn edit-btn">Редакт</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };

  return (
    <div className="complaints-list">
      <div className="list-controls">
        <select className="filter-select">
          <option value="all">Все статусы</option>
          <option value="open">Открытые</option>
          <option value="in_progress">В процессе</option>
          <option value="resolved">Решенные</option>
        </select>
        <select className="filter-select">
          <option value="all">Все приоритеты</option>
          <option value="low">Низкий</option>
          <option value="medium">Средний</option>
          <option value="high">Высокий</option>
        </select>
        <button className="refresh-btn" onClick={loadComplaints}>
          Обновить
        </button>
        <button className="add-btn">Добавить жалобу</button>
      </div>

      {renderContent()}
    </div>
  );
};

export { ComplaintsList };
