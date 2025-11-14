import React from "react";
import { useNavigate } from "react-router-dom";

interface HeaderProps {
  onLogout: () => void;
}

const Header: React.FC<HeaderProps> = ({ onLogout }) => {
  const navigate = useNavigate();
  const username = localStorage.getItem("username") || "Пользователь";

  const handleLogout = () => {
    onLogout();
    navigate("/login");
  };

  return (
    <header className="header">
      <div className="header-content">
        <div className="logo-section">
          <h1>Система мониторинга водоснабжения</h1>
        </div>
        <div className="user-section">
          <span className="user-name">Привет, {username}!</span>
          <button className="logout-btn" onClick={handleLogout}>
            Выйти
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;
