import React from "react";
import { Link } from "react-router-dom";

const HomePage: React.FC = () => {
  return (
    <div className="home-page">
      <div className="home-header">
        <h1>Система мониторинга водоснабжения</h1>
        <p>Добро пожаловать на главную страницу</p>
      </div>

      <div className="home-content">
        <div className="dashboard-sections">
          <div className="section-card">
            <h3>Инфраструктура водоснабжения</h3>
            <p>Просмотр состояния систем водоснабжения</p>
            <Link to="/water-infrastructure" className="view-link">
              Посмотреть
            </Link>
          </div>

          <div className="section-card">
            <h3>Качество воды</h3>
            <p>Просмотр данных о качестве воды</p>
            <Link to="/water-quality" className="view-link">
              Посмотреть
            </Link>
          </div>

          <div className="section-card">
            <h3>Активы</h3>
            <p>Просмотр активов системы водоснабжения</p>
            <Link to="/assets" className="view-link">
              Посмотреть
            </Link>
          </div>

          <div className="section-card">
            <h3>Прогнозирование спроса</h3>
            <p>Просмотр прогнозов спроса на воду</p>
            <Link to="/demand-forecasting" className="view-link">
              Посмотреть
            </Link>
          </div>
        </div>

        <div className="user-actions">
          <div className="section-card">
            <h3>Отправить жалобу</h3>
            <p>Сообщите о проблемах с водоснабжением</p>
            <Link to="/complaints" className="action-link">
              Отправить жалобу
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
