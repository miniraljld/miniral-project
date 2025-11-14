import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { userService } from "../api/userService";

interface LoginProps {
  onLogin: () => void;
}

const Login: React.FC<LoginProps> = ({ onLogin }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (username && password) {
      try {
        // Реальный вызов API для аутентификации
        const response = await userService.login({
          username,
          password,
        });

        // Сохраняем токен и информацию о пользователе
        localStorage.setItem("token", response.access_token);
        localStorage.setItem("username", response.username);

        onLogin();

        // Перенаправляем на дашборд
        navigate("/dashboard");
      } catch (err) {
        setError("Неверное имя пользователя или пароль");
        console.error("Ошибка аутентификации:", err);
      }
    } else {
      setError("Пожалуйста, заполните все поля");
    }
  };

  return (
    <div className="login-container">
      <div className="login-form">
        <h2>Вход в систему</h2>
        {error && <div className="error-message">{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">Имя пользователя:</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Пароль:</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="login-btn">
            Войти
          </button>
        </form>
        <div className="login-footer">
          <p>Демо-версия. Используйте любые данные для входа.</p>
          <p>
            Нет аккаунта? <a href="/register">Зарегистрироваться</a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
