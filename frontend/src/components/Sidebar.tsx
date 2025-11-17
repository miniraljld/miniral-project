import React from "react";
import { Link, useLocation } from "react-router-dom";

interface SidebarProps {
  currentUser?: {
    id: number;
    username: string;
    email: string;
    full_name?: string;
    is_active: boolean;
    role: "user" | "engineer" | "admin";
    created_at: string;
    updated_at?: string;
  } | null;
}

const Sidebar: React.FC<SidebarProps> = ({ currentUser }) => {
  const location = useLocation();

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  return (
    <aside className="sidebar">
      <nav className="nav-menu">
        <ul>
          <li>
            <Link
              to="/home"
              className={
                isActive("/home") || isActive("/dashboard") ? "active" : ""
              }
            >
              Главная
            </Link>
          </li>
          {/* Пункты меню для обычных пользователей (только просмотр) */}
          <li>
            <Link
              to="/water-infrastructure"
              className={isActive("/water-infrastructure") ? "active" : ""}
            >
              Инфраструктура
            </Link>
          </li>
          <li>
            <Link
              to="/water-quality"
              className={isActive("/water-quality") ? "active" : ""}
            >
              Качество воды
            </Link>
          </li>
          <li>
            <Link to="/assets" className={isActive("/assets") ? "active" : ""}>
              Активы
            </Link>
          </li>
          <li>
            <Link
              to="/demand-forecasting"
              className={isActive("/demand-forecasting") ? "active" : ""}
            >
              Прогнозирование
            </Link>
          </li>
          {/* Пункт меню для всех пользователей */}
          <li>
            <Link
              to="/complaints"
              className={isActive("/complaints") ? "active" : ""}
            >
              Жалобы
            </Link>
          </li>

          {/* Пункты меню для инженеров и администраторов (админка) */}
          {(currentUser?.role === "engineer" ||
            currentUser?.role === "admin") && (
            <>
              <li className="admin-section-header">Администрирование</li>
              <li>
                <Link
                  to="/admin/users"
                  className={isActive("/admin/users") ? "active" : ""}
                >
                  Управление пользователями
                </Link>
              </li>
              <li>
                <Link
                  to="/admin/water-infrastructure"
                  className={
                    isActive("/admin/water-infrastructure") ? "active" : ""
                  }
                >
                  Управление инфраструктурой
                </Link>
              </li>
              <li>
                <Link
                  to="/admin/water-quality"
                  className={isActive("/admin/water-quality") ? "active" : ""}
                >
                  Управление качеством воды
                </Link>
              </li>
              <li>
                <Link
                  to="/admin/assets"
                  className={isActive("/admin/assets") ? "active" : ""}
                >
                  Управление активами
                </Link>
              </li>
              <li>
                <Link
                  to="/admin/demand-forecasting"
                  className={
                    isActive("/admin/demand-forecasting") ? "active" : ""
                  }
                >
                  Управление прогнозированием
                </Link>
              </li>
              <li>
                <Link
                  to="/admin/notifications"
                  className={isActive("/admin/notifications") ? "active" : ""}
                >
                  Управление уведомлениями
                </Link>
              </li>
            </>
          )}
        </ul>
      </nav>
    </aside>
  );
};

export default Sidebar;
