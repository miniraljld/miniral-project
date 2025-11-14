import React from "react";
import { AssetManagement } from "../components/AssetManagement";

const AssetsPage: React.FC = () => {
  return (
    <div className="page-container">
      <h2>Управление активами</h2>
      <AssetManagement />
    </div>
  );
};

export default AssetsPage;
