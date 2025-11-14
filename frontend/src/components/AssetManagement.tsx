import React, { useState, useEffect, useCallback } from "react";
import { assetsService } from "../api/assetsService";
import type { WaterAsset } from "../api/types";

const AssetManagement: React.FC = () => {
  const [assets, setAssets] = useState<WaterAsset[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadAssets = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await assetsService.getAllAssets(0, 50);
      setAssets(data);
    } catch (err) {
      console.error("Ошибка загрузки активов:", err);
      setError("Не удалось загрузить активы. Проверьте API.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadAssets();
  }, [loadAssets]);

  const getStatusColor = (status?: string) => {
    switch (status) {
      case "operational":
        return "#4CAF50";
      case "maintenance_required":
        return "#FFC107";
      case "out_of_service":
        return "#F44336";
      default:
        return "#9E9E9E";
    }
  };

  const getStatusText = (status?: string) => {
    switch (status) {
      case "operational":
        return "Работает";
      case "maintenance_required":
        return "Требует обслуживания";
      case "out_of_service":
        return "Вне эксплуатации";
      default:
        return "Неизвестно";
    }
  };

  const formatDate = (date?: string) => {
    return date ? new Date(date).toLocaleDateString() : "—";
  };

  const renderContent = () => {
    if (loading) {
      return <p>Загрузка списка активов...</p>;
    }

    if (error) {
      return (
        <div className="error-state">
          <p>{error}</p>
          <button className="refresh-btn" onClick={loadAssets}>
            Повторить
          </button>
        </div>
      );
    }

    if (assets.length === 0) {
      return <p>Активы отсутствуют. Добавьте их через backend API.</p>;
    }

    return (
      <div className="assets-table">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Название</th>
              <th>Тип</th>
              <th>Местоположение</th>
              <th>Статус</th>
              <th>Дата установки</th>
              <th>Последнее обслуживание</th>
              <th>Следующее обслуживание</th>
              <th>В эксплуатации</th>
              <th>Стоимость</th>
            </tr>
          </thead>
          <tbody>
            {assets.map((asset) => (
              <tr key={asset.id}>
                <td>{asset.id}</td>
                <td>{asset.name}</td>
                <td>{asset.asset_type}</td>
                <td>{asset.location}</td>
                <td>
                  <span
                    className="status-indicator"
                    style={{ backgroundColor: getStatusColor(asset.status) }}
                  >
                    {getStatusText(asset.status)}
                  </span>
                </td>
                <td>{formatDate(asset.installation_date)}</td>
                <td>{formatDate(asset.last_maintenance)}</td>
                <td>{formatDate(asset.next_maintenance)}</td>
                <td>{asset.is_operational ? "Да" : "Нет"}</td>
                <td>{asset.asset_value ? `${asset.asset_value} сом` : "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };

  return (
    <div className="asset-management">
      <div className="list-controls">
        <select className="filter-select">
          <option value="all">Все типы</option>
          <option value="pipe">Трубы</option>
          <option value="pump">Насосные станции</option>
          <option value="tank">Резервуары</option>
          <option value="equipment">Оборудование</option>
        </select>
        <select className="filter-select">
          <option value="all">Все статусы</option>
          <option value="operational">Работает</option>
          <option value="maintenance_required">Требует обслуживания</option>
          <option value="out_of_service">Вне эксплуатации</option>
        </select>
        <button className="refresh-btn" onClick={loadAssets}>
          Обновить
        </button>
        <button className="add-btn">Добавить актив</button>
      </div>

      {renderContent()}
    </div>
  );
};

export { AssetManagement };
