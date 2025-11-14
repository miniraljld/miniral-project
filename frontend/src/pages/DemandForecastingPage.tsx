import React from "react";
import { DemandForecasting } from "../components/DemandForecasting";

const DemandForecastingPage: React.FC = () => {
  return (
    <div className="page-container">
      <h2>Прогнозирование спроса</h2>
      <DemandForecasting />
    </div>
  );
};

export default DemandForecastingPage;
