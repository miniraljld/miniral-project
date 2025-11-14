import React, { useState, useEffect, useCallback } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import { userService } from "./api/userService";
import ProtectedRoute from "./components/ProtectedRoute";
import Dashboard from "./pages/Dashboard";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Layout from "./components/Layout";
import WaterInfrastructurePage from "./pages/WaterInfrastructurePage";
import WaterQualityPage from "./pages/WaterQualityPage";
import ComplaintsPage from "./pages/ComplaintsPage";
import AssetsPage from "./pages/AssetsPage";
import DemandForecastingPage from "./pages/DemandForecastingPage";
import NotificationsPage from "./pages/NotificationsPage";
import UsersPage from "./pages/UsersPage";
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
            element={
              <Navigate to={isAuthenticated ? "/dashboard" : "/login"} />
            }
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
            <Route path="/dashboard" element={<Dashboard />} />
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
            <Route path="/users" element={<UsersPage />} />
            <Route
              path="/admin/users"
              element={
                <ProtectedRoute requiredRole="admin" fallbackPath="/dashboard">
                  <AdminUsers />
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
