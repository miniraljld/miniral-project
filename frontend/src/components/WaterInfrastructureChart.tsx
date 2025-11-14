import React, { useEffect, useState, useCallback } from "react";
import { waterInfrastructureService } from "../api/waterInfrastructureService";
import type { WaterInfrastructure } from "../api/types";

const WaterInfrastructureChart: React.FC = () => {
  const [infrastructureData, setInfrastructureData] = useState<
    WaterInfrastructure[]
  >([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadInfrastructure = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await waterInfrastructureService.getAllInfrastructure(
        0,
        50
      );
      setInfrastructureData(data);
    } catch (err) {
      console.error("Ошибка загрузки инфраструктуры:", err);
      setError("Не удалось загрузить инфраструктуру. Проверьте API.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadInfrastructure();
  }, [loadInfrastructure]);

  const getStatusColor = (status?: string) => {
    switch (status) {
      case "good":
      case "operational":
        return "#4CAF50";
      case "warning":
      case "degraded":
        return "#FFC107";
      case "critical":
      case "out_of_service":
        return "#F44336";
      default:
        return "#9E9E9E";
    }
  };

  const renderContent = () => {
    if (loading) {
      return <p>Загрузка объектов инфраструктуры...</p>;
    }

    if (error) {
      return (
        <div className="error-state">
          <p>{error}</p>
          <button className="refresh-btn" onClick={loadInfrastructure}>
            Повторить
          </button>
        </div>
      );
    }

    if (infrastructureData.length === 0) {
      return <p>Нет данных об инфраструктуре. Добавьте объекты через API.</p>;
    }

    return (
      <div className="infrastructure-list">
        {infrastructureData.map((item) => (
          <div key={item.id} className="infrastructure-item">
            <div className="item-header">
              <h4>{item.name}</h4>
              <span
                className="status-indicator"
                style={{ backgroundColor: getStatusColor(item.condition_status) }}
                title={item.condition_status}
              />
            </div>
            <div className="item-details">
              <p>
                <strong>Тип:</strong> {item.type}
              </p>
              <p>
                <strong>Местоположение:</strong> {item.location}
              </p>
              <p>
                <strong>Статус:</strong>{" "}
                <span
                  style={{
                    color: getStatusColor(item.condition_status),
                    fontWeight: "bold",
                  }}
                >
                  {item.condition_status || "Не указан"}
                </span>
              </p>
              {typeof item.pressure === "number" && (
                <p>
                  <strong>Давление:</strong> {item.pressure} бар
                </p>
              )}
              {typeof item.temperature === "number" && (
                <p>
                  <strong>Температура:</strong> {item.temperature} °C
                </p>
              )}
              <p>
                <strong>Утечка:</strong>{" "}
                {item.leak_detected ? (
                  <span style={{ color: "#F44336", fontWeight: "bold" }}>
                    ДА
                  </span>
                ) : (
                  "НЕТ"
                )}
              </p>
              {item.last_inspection && (
                <p>
                  <strong>Последняя проверка:</strong>{" "}
                  {new Date(item.last_inspection).toLocaleDateString()}
                </p>
              )}
            </div>
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="water-infrastructure-chart">
      <div className="chart-controls">
        <select className="filter-select">
          <option value="all">Все типы</option>
          <option value="pipe">Трубы</option>
          <option value="pump">Насосные станции</option>
          <option value="tank">Резервуары</option>
          <option value="equipment">Оборудование</option>
        </select>
        <button className="refresh-btn" onClick={loadInfrastructure}>
          Обновить данные
        </button>
        <button className="add-btn">Добавить объект</button>
      </div>

      {renderContent()}
    </div>
  );
};

export { WaterInfrastructureChart };
