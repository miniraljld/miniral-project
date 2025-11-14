import React from "react";
import { ComplaintsList } from "../components/ComplaintsList";

const ComplaintsPage: React.FC = () => {
  return (
    <div className="page-container">
      <h2>Жалобы и обращения</h2>
      <ComplaintsList />
    </div>
  );
};

export default ComplaintsPage;
