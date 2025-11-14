import React from "react";
import { WaterInfrastructureChart } from "../components/WaterInfrastructureChart";

const WaterInfrastructurePage: React.FC = () => {
  return (
    <div className="page-container">
      <h2>Инфраструктура водоснабжения</h2>
      <WaterInfrastructureChart />
    </div>
  );
};

export default WaterInfrastructurePage;
