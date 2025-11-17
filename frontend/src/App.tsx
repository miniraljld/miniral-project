import React, { useState, useEffect, useCallback } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import { userService } from "./api/userService";
import ProtectedRoute from "./components/ProtectedRoute";
import HomePage from "./pages/HomePage";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Layout from "./components/Layout";
import WaterInfrastructurePage from "./pages/WaterInfrastructurePage";
import WaterQualityPage from "./pages/WaterQualityPage";
import ComplaintsPage from "./pages/ComplaintsPage";
import AssetsPage from "./pages/AssetsPage";
import DemandForecastingPage from "./pages/DemandForecastingPage";
import NotificationsPage from "./pages/NotificationsPage";
import AdminUsers from "./pages/AdminUsers";
import "./App.css";

interface User {
  id: number;
  username: string;
  email: string;
  full_name?: string;
  is_active: boolean;
  role: "user" | "engineer" | "admin";
  created_at: string;
  updated_at?: string;
}

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(() => {
    return !!localStorage.getItem("token");
  });
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const syncAuthState = useCallback(async () => {
    const token = localStorage.getItem("token");
    setIsAuthenticated(!!token);

    if (token && userService.getCurrentUser) {
      try {
        const user = await userService.getCurrentUser();
        setCurrentUser(user);
      } catch (error) {
        console.error("Ошибка получения информации о пользователе:", error);
        setCurrentUser(null);
      }
    } else {
      setCurrentUser(null);
    }
  }, []);

  const handleLogin = useCallback(async () => {
    setIsAuthenticated(true);

    // Загружаем информацию о текущем пользователе
    try {
      const user = await userService.getCurrentUser();
      setCurrentUser(user);
      localStorage.setItem("userRole", user.role);
    } catch (error) {
      console.error("Ошибка получения информации о пользователе:", error);
    }
  }, []);

  const handleLogout = useCallback(() => {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    localStorage.removeItem("userRole");
    setCurrentUser(null);
    setIsAuthenticated(false);
  }, []);

  // Проверяем аутентификацию при загрузке приложения
  useEffect(() => {
    syncAuthState();
    setLoading(false);
  }, [syncAuthState]);

  if (loading) {
    return <div className="app-loading">Загрузка приложения...</div>;
  }

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route
            path="/login"
            element={
              isAuthenticated ? (
                <Navigate to="/dashboard" />
              ) : (
                <Login onLogin={handleLogin} />
              )
            }
          />
          <Route
            path="/register"
            element={
              isAuthenticated ? (
                <Navigate to="/dashboard" />
              ) : (
                <Register onRegister={handleLogin} />
              )
            }
          />
          <Route
            path="/"
            element={<Navigate to={isAuthenticated ? "/home" : "/login"} />}
          />
          <Route
            path="/"
            element={
              isAuthenticated ? (
                <Layout onLogout={handleLogout} currentUser={currentUser} />
              ) : (
                <Navigate to="/login" />
              )
            }
          >
            {/* Маршруты для обычных пользователей */}
            <Route path="/dashboard" element={<HomePage />} />
            <Route path="/home" element={<HomePage />} />
            {/* Маршрут для администраторов */}
            <Route path="/admin" element={<Navigate to="/admin/users" />} />
            <Route
              path="/water-infrastructure"
              element={<WaterInfrastructurePage />}
            />
            <Route path="/water-quality" element={<WaterQualityPage />} />
            <Route path="/complaints" element={<ComplaintsPage />} />
            <Route path="/assets" element={<AssetsPage />} />
            <Route
              path="/demand-forecasting"
              element={<DemandForecastingPage />}
            />
            <Route path="/notifications" element={<NotificationsPage />} />

            {/* Маршруты для администраторов и инженеров */}
            <Route
              path="/admin/users"
              element={
                <ProtectedRoute requiredRole="admin" fallbackPath="/home">
                  <AdminUsers />
                </ProtectedRoute>
              }
            />
            <Route
              path="/admin/water-infrastructure"
              element={
                <ProtectedRoute requiredRole="admin" fallbackPath="/home">
                  <WaterInfrastructurePage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/admin/water-quality"
              element={
                <ProtectedRoute requiredRole="admin" fallbackPath="/home">
                  <WaterQualityPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/admin/complaints"
              element={
                <ProtectedRoute requiredRole="admin" fallbackPath="/home">
                  <ComplaintsPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/admin/assets"
              element={
                <ProtectedRoute requiredRole="admin" fallbackPath="/home">
                  <AssetsPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/admin/demand-forecasting"
              element={
                <ProtectedRoute requiredRole="admin" fallbackPath="/home">
                  <DemandForecastingPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/admin/notifications"
              element={
                <ProtectedRoute requiredRole="admin" fallbackPath="/home">
                  <NotificationsPage />
                </ProtectedRoute>
              }
            />
          </Route>
        </Routes>
      </div>
    </Router>
  );
}

export default App;
