import React, { useCallback, useEffect, useState } from "react";
import { demandForecastingService } from "../api/demandForecastingService";
import type { WaterDemand, WaterDistributionPlan } from "../api/types";

const DemandForecasting: React.FC = () => {
  const [demandData, setDemandData] = useState<WaterDemand[]>([]);
  const [distributionPlans, setDistributionPlans] = useState<
    WaterDistributionPlan[]
  >([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadDemandData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [demand, plans] = await Promise.all([
        demandForecastingService.getAllDemandData(0, 50),
        demandForecastingService.getAllDistributionPlans(0, 50),
      ]);
      setDemandData(demand);
      setDistributionPlans(plans);
    } catch (err) {
      console.error("Ошибка загрузки данных спроса:", err);
      setError("Не удалось загрузить данные о спросе и планах распределения.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadDemandData();
  }, [loadDemandData]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case "draft":
        return "#9E9E9E"; // Серый
      case "planned":
        return "#2196F3"; // Синий
      case "active":
        return "#4CAF50"; // Зеленый
      case "completed":
        return "#8BC34A"; // Светло-зеленый
      default:
        return "#9E9E9E"; // Серый
    }
  };

  const getDemandTypeColor = (type: string) => {
    switch (type) {
      case "residential":
        return "#2196F3"; // Синий
      case "commercial":
        return "#FF9800"; // Оранжевый
      case "industrial":
        return "#9C27B0"; // Фиолетовый
      case "public":
        return "#00BCD4"; // Бирюзовый
      default:
        return "#9E9E9E"; // Серый
    }
  };

  if (loading) {
    return <p>Загрузка прогнозов и планов...</p>;
  }

  if (error) {
    return (
      <div className="error-state">
        <p>{error}</p>
        <button className="refresh-btn" onClick={loadDemandData}>
          Повторить
        </button>
      </div>
    );
  }

  return (
    <div className="demand-forecasting">
      <div className="list-controls">
        <select className="filter-select">
          <option value="all">Все типы</option>
          <option value="residential">Жилой сектор</option>
          <option value="commercial">Коммерческий сектор</option>
          <option value="industrial">Промышленный сектор</option>
          <option value="public">Общественный сектор</option>
        </select>
        <select className="filter-select">
          <option value="all">Все статусы</option>
          <option value="draft">Черновик</option>
          <option value="planned">Запланирован</option>
          <option value="active">Активен</option>
          <option value="completed">Завершен</option>
        </select>
        <button className="refresh-btn" onClick={loadDemandData}>
          Обновить
        </button>
        <button className="add-btn">Добавить план</button>
      </div>
      <div className="forecasting-content">
        <div className="demand-section">
          <h3>Прогнозируемый спрос на воду</h3>
          <div className="demand-list">
            {demandData.map((demand) => (
              <div key={demand.id} className="demand-item">
                <div className="demand-header">
                  <h4>{demand.location}</h4>
                  <span
                    className="type-indicator"
                    style={{
                      backgroundColor: getDemandTypeColor(demand.demand_type),
                    }}
                  >
                    {demand.demand_type}
                  </span>
                </div>
                <div className="demand-details">
                  <p>
                    <strong>Объем:</strong> {demand.demand_amount} м³
                  </p>
                  <p>
                    <strong>Дата:</strong>{" "}
                    {new Date(demand.demand_date).toLocaleDateString()}
                  </p>
                  <p>
                    <strong>Прогноз:</strong>{" "}
                    {demand.forecasted ? "Да" : "Нет"}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="distribution-section">
          <h3>Планы распределения</h3>
          <div className="distribution-table">
            <table>
              <thead>
                <tr>
                  <th>Название плана</th>
                  <th>Описание</th>
                  <th>Период</th>
                  <th>Всего воды</th>
                  <th>Жилой сектор</th>
                  <th>Коммерческий</th>
                  <th>Промышленный</th>
                  <th>Общественный</th>
                  <th>Статус</th>
                </tr>
              </thead>
              <tbody>
                {distributionPlans.map((plan) => (
                  <tr key={plan.id}>
                    <td>{plan.plan_name}</td>
                    <td>{plan.description}</td>
                    <td>
                      {new Date(plan.start_date).toLocaleDateString()} -{" "}
                      {new Date(plan.end_date).toLocaleDateString()}
                    </td>
                    <td>{plan.total_water_allocated} м³</td>
                    <td>{plan.allocated_to_residential} м³</td>
                    <td>{plan.allocated_to_commercial} м³</td>
                    <td>{plan.allocated_to_industrial} м³</td>
                    <td>{plan.allocated_to_public} м³</td>
                    <td>
                      <span
                        className="status-indicator"
                        style={{ backgroundColor: getStatusColor(plan.status) }}
                      >
                        {plan.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export { DemandForecasting };
