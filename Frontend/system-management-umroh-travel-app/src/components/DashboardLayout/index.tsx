// src/components/DashboardLayout.tsx (Pembaruan untuk Sidebar Desktop)

import { useAuth } from "@/hooks/useAuth";
import { Header } from "../Header";
import { Sidebar } from "../Sidebar";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
interface DashboardLayoutProps {
  children: React.ReactNode;
}

// Ubah cara Anda mendefinisikan komponen
// Gunakan tipe data 'DashboardLayoutProps' untuk props
export function DashboardLayout({ children }: DashboardLayoutProps) {
  const {
    handleLogout,
    isAuthenticated,
    userData,
    isUserDataLoading,
    handleFetchUserData,
    error,
  } = useAuth();
  const navigate = useNavigate();
  const [isLoggingOut, setIsLoggingOut] = useState(false);
  const handleLogoutClick = async () => {
    setIsLoggingOut(true);
    try {
      await new Promise((resolve) => setTimeout(resolve, 500));
      handleLogout();
      navigate("/login");
    } catch (error) {
      console.error("Logout failed:", error);
    } finally {
      setIsLoggingOut(false);
    }
  };
  return (
    <div className="flex h-screen bg-gray-50 dark:bg-gray-900">
      {/* 1. Sidebar (Hanya Desktop) */}
      {/* Meneruskan class Tailwind: hidden di layar kecil, flex dan lebar 64 di layar besar */}
      <Sidebar className="hidden lg:flex w-64" />

      <div className="flex flex-col flex-1 overflow-hidden">
        {/* 2. Header / Navbar */}
        <Header
          handleLogoutClick={handleLogoutClick}
          isLoggingOut={isLoggingOut}
          userData={userData}
        />

        {/* 3. Main Content Area */}
        <main className="flex-1 overflow-x-hidden overflow-y-auto p-6">
          {children}
        </main>
      </div>
    </div>
  );
}
