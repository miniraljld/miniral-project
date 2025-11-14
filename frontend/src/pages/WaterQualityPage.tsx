import React from "react";
import { WaterQualityChart } from "../components/WaterQualityChart";

const WaterQualityPage: React.FC = () => {
  return (
    <div className="page-container">
      <h2>Качество воды</h2>
      <WaterQualityChart />
    </div>
  );
};

export default WaterQualityPage;
