import React, { useCallback, useEffect, useState } from "react";
import { waterQualityService } from "../api/waterQualityService";
import type { WaterQuality } from "../api/types";

const WaterQualityChart: React.FC = () => {
  const [waterQualityData, setWaterQualityData] = useState<WaterQuality[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadWaterQuality = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await waterQualityService.getAllQualityData(0, 50);
      setWaterQualityData(data);
    } catch (err) {
      console.error("Ошибка загрузки качества воды:", err);
      setError("Не удалось загрузить данные о качестве воды.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadWaterQuality();
  }, [loadWaterQuality]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case "good":
        return "#4CAF50"; // Зеленый
      case "warning":
        return "#FFC107"; // Желтый
      case "critical":
        return "#F44336"; // Красный
      default:
        return "#9E9E9E"; // Серый
    }
  };

  const getQualityStatusText = (status: string) => {
    switch (status) {
      case "good":
        return "Хорошее";
      case "warning":
        return "Предупреждение";
      case "critical":
        return "Критическое";
      default:
        return "Неизвестно";
    }
  };

  const renderContent = () => {
    if (loading) {
      return <p>Загрузка данных о качестве воды...</p>;
    }

    if (error) {
      return (
        <div className="error-state">
          <p>{error}</p>
          <button className="refresh-btn" onClick={loadWaterQuality}>
            Повторить
          </button>
        </div>
      );
    }

    if (waterQualityData.length === 0) {
      return <p>Нет измерений качества воды. Добавьте данные через API.</p>;
    }

    return (
      <div className="quality-list">
        {waterQualityData.map((item) => (
          <div key={item.id} className="quality-item">
            <div className="item-header">
              <h4>{item.location}</h4>
              <span
                className="status-indicator"
                style={{ backgroundColor: getStatusColor(item.quality_status) }}
                title={item.quality_status}
              />
            </div>
            <div className="item-details">
              <p>
                <strong>Дата измерения:</strong>{" "}
                {new Date(item.date_measured).toLocaleString()}
              </p>
              {typeof item.ph_level === "number" && (
                <p>
                  <strong>Уровень pH:</strong> {item.ph_level} (норма: 6.5-8.5)
                </p>
              )}
              {typeof item.chlorine_level === "number" && (
                <p>
                  <strong>Хлор:</strong> {item.chlorine_level} мг/л (норма:
                  0.2-1.0)
                </p>
              )}
              {typeof item.turbidity === "number" && (
                <p>
                  <strong>Мутность:</strong> {item.turbidity} NTU (норма: &lt;
                  1.0)
                </p>
              )}
              {typeof item.dissolved_oxygen === "number" && (
                <p>
                  <strong>Растворенный кислород:</strong>{" "}
                  {item.dissolved_oxygen} мг/л
                </p>
              )}
              {typeof item.e_coli === "number" && (
                <p>
                  <strong>Коли-формы:</strong> {item.e_coli} КОЕ/100мл (норма:
                  0)
                </p>
              )}
              <p>
                <strong>Статус качества:</strong>{" "}
                <span
                  style={{
                    color: getStatusColor(item.quality_status),
                    fontWeight: "bold",
                  }}
                >
                  {getQualityStatusText(item.quality_status)}
                </span>
              </p>
              {item.notes && (
                <p>
                  <strong>Комментарий:</strong> {item.notes}
                </p>
              )}
            </div>
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="water-quality-chart">
      <div className="chart-controls">
        <select className="filter-select">
          <option value="all">Все локации</option>
          <option value="reservoir">Резервуары</option>
          <option value="district">Районы</option>
        </select>
        <button className="refresh-btn" onClick={loadWaterQuality}>
          Обновить данные
        </button>
      </div>

      {renderContent()}
    </div>
  );
};

export { WaterQualityChart };
