import React from "react";
import { Outlet } from "react-router-dom";
import Header from "./Header";
import Sidebar from "./Sidebar";

interface LayoutProps {
  onLogout: () => void;
  currentUser?: {
    id: number;
    username: string;
    email: string;
    full_name?: string;
    is_active: boolean;
    role: "user" | "engineer" | "admin";
    created_at: string;
    updated_at?: string;
  } | null;
}

const Layout: React.FC<LayoutProps> = ({ onLogout, currentUser }) => {
  return (
    <div className="app-layout">
      <Header onLogout={onLogout} />
      <div className="main-content">
        <Sidebar currentUser={currentUser} />
        <main className="content">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default Layout;
