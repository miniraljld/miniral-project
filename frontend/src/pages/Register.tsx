import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { userService } from "../api/userService";

interface RegisterProps {
  onRegister: () => void;
}

const Register: React.FC<RegisterProps> = ({ onRegister }) => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [fullName, setFullName] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const navigate = useNavigate();

  const validateForm = () => {
    if (!username.trim()) {
      setError("Имя пользователя обязательно");
      return false;
    }

    if (!email.trim()) {
      setError("Email обязателен");
      return false;
    }

    if (!password.trim()) {
      setError("Пароль обязателен");
      return false;
    }

    if (password.length < 6) {
      setError("Пароль должен содержать не менее 6 символов");
      return false;
    }

    if (password !== confirmPassword) {
      setError("Пароли не совпадают");
      return false;
    }

    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    try {
      await userService.createUser({
        username,
        email,
        full_name: fullName,
        password,
        is_active: true,
        role: "user",
      });

      setSuccess(
        "Регистрация прошла успешно! Теперь вы можете войти в систему."
      );
      setError("");

      // Очищаем форму
      setUsername("");
      setEmail("");
      setFullName("");
      setPassword("");
      setConfirmPassword("");

      // Перенаправляем на страницу входа через 2 секунды
      setTimeout(() => {
        navigate("/login");
      }, 2000);
    } catch (err: any) {
      if (err.response && err.response.data && err.response.data.detail) {
        setError(err.response.data.detail);
      } else {
        setError("Ошибка при регистрации. Пожалуйста, попробуйте еще раз.");
      }
      console.error("Ошибка регистрации:", err);
    }
  };

  return (
    <div className="register-container">
      <div className="register-form">
        <h2>Регистрация</h2>

        {error && <div className="error-message">{error}</div>}
        {success && <div className="success-message">{success}</div>}

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
            <label htmlFor="email">Email:</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="fullName">Полное имя:</label>
            <input
              type="text"
              id="fullName"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
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
              minLength={6}
            />
          </div>

          <div className="form-group">
            <label htmlFor="confirmPassword">Подтверждение пароля:</label>
            <input
              type="password"
              id="confirmPassword"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
          </div>

          <button type="submit" className="register-btn">
            Зарегистрироваться
          </button>
        </form>

        <div className="register-footer">
          <p>
            Уже есть аккаунт? <a href="/login">Войти</a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Register;
