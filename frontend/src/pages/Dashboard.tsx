import React, { useState, useEffect, useCallback } from "react";
import { WaterInfrastructureChart } from "../components/WaterInfrastructureChart";
import { WaterQualityChart } from "../components/WaterQualityChart";
import { ComplaintsList } from "../components/ComplaintsList";
import { AssetManagement } from "../components/AssetManagement";
import { DemandForecasting } from "../components/DemandForecasting";
import { NotificationPanel } from "../components/NotificationPanel";
import { userService } from "../api/userService";
import { waterInfrastructureService } from "../api/waterInfrastructureService";
import { waterQualityService } from "../api/waterQualityService";
import { complaintsService } from "../api/complaintsService";
import { assetsService } from "../api/assetsService";
import { demandForecastingService } from "../api/demandForecastingService";
import { notificationsService } from "../api/notificationsService";
import type {
  User,
  WaterAsset,
  WaterInfrastructure,
  WaterQuality,
  Complaint,
  Notification,
  WaterDemand,
} from "../api/types";

interface DashboardMetrics {
  totalUsers: number;
  activeLeaks: number;
  waterQualityIssues: number;
  complaints: number;
  assets: number;
  maintenanceTasks: number;
  pendingNotifications: number;
  demandRecords: number;
}

const Dashboard: React.FC = () => {
  const [dashboardData, setDashboardData] = useState<DashboardMetrics | null>(
    null
  );
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const calculateMaintenanceTasks = (assets: WaterAsset[]) => {
    const now = new Date();
    return assets.filter((asset) => {
      if (!asset.next_maintenance) {
        return false;
      }
      const nextDate = new Date(asset.next_maintenance);
      return nextDate <= now;
    }).length;
  };

  const calculateWaterQualityIssues = (quality: WaterQuality[]) => {
    return quality.filter(
      (measurement) => measurement.quality_status && measurement.quality_status !== "good"
    ).length;
  };

  const fetchDashboardData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [
        users,
        infrastructure,
        quality,
        complaints,
        assets,
        demand,
        notifications,
      ] = await Promise.all([
        userService.getUsers(0, 50) as Promise<User[]>,
        waterInfrastructureService.getAllInfrastructure(0, 50) as Promise<
          WaterInfrastructure[]
        >,
        waterQualityService.getAllQualityData(0, 50) as Promise<WaterQuality[]>,
        complaintsService.getAllComplaints(0, 50) as Promise<Complaint[]>,
        assetsService.getAllAssets(0, 50) as Promise<WaterAsset[]>,
        demandForecastingService.getAllDemandData(0, 50) as Promise<
          WaterDemand[]
        >,
        notificationsService.getUserNotifications(0, 50) as Promise<
          Notification[]
        >,
      ]);

      const activeLeaks = infrastructure.filter((item) => item.leak_detected)
        .length;
      const maintenanceTasks = calculateMaintenanceTasks(assets);
      const qualityIssues = calculateWaterQualityIssues(quality);
      const pendingNotifications = notifications.filter(
        (notification) => !notification.is_read
      ).length;

      setDashboardData({
        totalUsers: users.length,
        activeLeaks,
        waterQualityIssues: qualityIssues,
        complaints: complaints.length,
        assets: assets.length,
        maintenanceTasks,
        pendingNotifications,
        demandRecords: demand.length,
      });
    } catch (err) {
      console.error("Ошибка загрузки данных дашборда:", err);
      setError("Не удалось загрузить данные. Проверьте подключение к API.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchDashboardData();
  }, [fetchDashboardData]);

  const renderState = () => {
    if (loading) {
      return (
        <div className="dashboard-loading">
          <h2>Загрузка дашборда...</h2>
          <p>Пожалуйста, подождите</p>
        </div>
      );
    }

    if (error) {
      return (
        <div className="dashboard-error">
          <p>{error}</p>
          <button className="refresh-btn" onClick={fetchDashboardData}>
            Повторить попытку
          </button>
        </div>
      );
    }

    if (!dashboardData) {
      return null;
    }

    return (
      <>
        <div className="dashboard-actions">
          <button className="refresh-btn" onClick={fetchDashboardData}>
            Обновить данные
          </button>
        </div>
        <div className="dashboard-metrics">
          <div className="metric-card">
            <h3>Пользователи</h3>
            <p className="metric-value">{dashboardData.totalUsers}</p>
          </div>
          <div className="metric-card">
            <h3>Активные утечки</h3>
            <p className="metric-value warning">{dashboardData.activeLeaks}</p>
          </div>
          <div className="metric-card">
            <h3>Проблемы с качеством</h3>
            <p className="metric-value warning">
              {dashboardData.waterQualityIssues}
            </p>
          </div>
          <div className="metric-card">
            <h3>Жалобы</h3>
            <p className="metric-value">{dashboardData.complaints}</p>
          </div>
          <div className="metric-card">
            <h3>Активы</h3>
            <p className="metric-value">{dashboardData.assets}</p>
          </div>
          <div className="metric-card">
            <h3>Задачи по обслуживанию</h3>
            <p className="metric-value">
              {dashboardData.maintenanceTasks}
            </p>
          </div>
          <div className="metric-card">
            <h3>Непрочитанные уведомления</h3>
            <p className="metric-value">{dashboardData.pendingNotifications}</p>
          </div>
          <div className="metric-card">
            <h3>Записи спроса</h3>
            <p className="metric-value">{dashboardData.demandRecords}</p>
          </div>
        </div>
      </>
    );
  };

  return (
    <div className="page-container">
      <h1>Дашборд мониторинга водоснабжения</h1>

      {renderState()}

      {/* Графики и визуализации */}
      <div className="dashboard-charts">
        <div className="chart-section">
          <h2>Инфраструктура водоснабжения</h2>
          <WaterInfrastructureChart />
        </div>

        <div className="chart-section">
          <h2>Качество воды</h2>
          <WaterQualityChart />
        </div>
      </div>

      {/* Список жалоб */}
      <div className="dashboard-section">
        <h2>Последние жалобы</h2>
        <ComplaintsList />
      </div>

      {/* Управление активами */}
      <div className="dashboard-section">
        <h2>Управление активами</h2>
        <AssetManagement />
      </div>

      {/* Прогнозирование спроса */}
      <div className="dashboard-section">
        <h2>Прогнозирование спроса</h2>
        <DemandForecasting />
      </div>

      {/* Панель уведомлений */}
      <div className="dashboard-section">
        <h2>Уведомления</h2>
        <NotificationPanel />
      </div>
    </div>
  );
};

export default Dashboard;
