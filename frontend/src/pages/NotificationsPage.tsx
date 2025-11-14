import React from "react";
import { NotificationPanel } from "../components/NotificationPanel";

const NotificationsPage: React.FC = () => {
  return (
    <div className="page-container">
      <h2>Уведомления</h2>
      <NotificationPanel />
    </div>
  );
};

export default NotificationsPage;
