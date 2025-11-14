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
              to="/dashboard"
              className={isActive("/dashboard") ? "active" : ""}
            >
              Дашборд
            </Link>
          </li>
          {/* Пункты меню для инженеров и администраторов */}
          {(currentUser?.role === "engineer" ||
            currentUser?.role === "admin") && (
            <>
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
                <Link
                  to="/assets"
                  className={isActive("/assets") ? "active" : ""}
                >
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
              <li>
                <Link
                  to="/notifications"
                  className={isActive("/notifications") ? "active" : ""}
                >
                  Уведомления
                </Link>
              </li>
            </>
          )}
          {/* Пункт меню для всех пользователей */}
          <li>
            <Link
              to="/complaints"
              className={isActive("/complaints") ? "active" : ""}
            >
              Жалобы
            </Link>
          </li>
          {/* Пункт меню только для администраторов */}
          {currentUser?.role === "admin" && (
            <li>
              <Link
                to="/admin/users"
                className={isActive("/admin/users") ? "active" : ""}
              >
                Управление пользователями
              </Link>
            </li>
          )}
        </ul>
      </nav>
    </aside>
  );
};

export default Sidebar;
