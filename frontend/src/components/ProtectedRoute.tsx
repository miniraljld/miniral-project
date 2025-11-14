import React from "react";
import { Navigate } from "react-router-dom";
import { userService } from "../api/userService";

interface ProtectedRouteProps {
  children: React.ReactNode;
  requiredRole?: "user" | "engineer" | "admin";
  fallbackPath?: string;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  children,
  requiredRole = "admin",
  fallbackPath = "/dashboard",
}) => {
  const token = localStorage.getItem("token");

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  // Проверяем, является ли пользователь администратором
  const userRole = localStorage.getItem("userRole");

  if (!userRole) {
    // Если роли нет в localStorage, пробуем получить её через API
    const fetchUserRole = async () => {
      try {
        const user = await userService.getCurrentUser();
        localStorage.setItem("userRole", user.role);
        // После установки роли перезагружаем страницу для обновления интерфейса
        window.location.reload();
      } catch (error) {
        console.error("Ошибка получения информации о пользователе:", error);
        localStorage.removeItem("token");
        localStorage.removeItem("username");
        localStorage.removeItem("userRole");
        window.location.href = "/login";
      }
    };

    fetchUserRole();
    return <div>Загрузка информации о пользователе...</div>;
  }

  if (requiredRole === "admin" && userRole !== "admin") {
    return <Navigate to={fallbackPath} replace />;
  }

  if (
    requiredRole === "engineer" &&
    !["engineer", "admin"].includes(userRole)
  ) {
    return <Navigate to={fallbackPath} replace />;
  }

  return <>{children}</>;
};

export default ProtectedRoute;
