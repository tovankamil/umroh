// src/components/Sidebar.tsx
import React from "react";
import { Home, User, Wallet, FileText, Clock } from "lucide-react";
import { Link } from "react-router-dom"; // Asumsi menggunakan React Router
import { cn } from "@/lib/utils"; // Fungsi cn dari shadcn/ui

const navItems = [
  { name: "Home", icon: Home, path: "/" },
  { name: "Profile", icon: User, path: "/profile" },
  { name: "Wallet", icon: Wallet, path: "/wallet" },
  { name: "Report", icon: FileText, path: "/report" },
  { name: "History", icon: Clock, path: "/history" },
];

interface SidebarProps {
  className?: string;
}

// Komponen sekarang menerima className
export function Sidebar({ className }: SidebarProps) {
  return (
    // Gunakan fungsi cn untuk menggabungkan default class dengan class dari prop
    <div
      className={cn(
        "flex flex-col border-r h-full bg-background p-4",
        className
      )}
    >
      {/* Judul/Logo */}
      <h1 className="text-xl font-bold mb-6 mt-4 px-2">Dashboard App</h1>

      {/* Menu Navigasi */}
      <nav className="flex flex-col space-y-2">
        {navItems.map((item) => (
          <Link
            key={item.name}
            to={item.path}
            // Tambahkan class agar tombol menempati lebar penuh
            className="flex items-center space-x-3 p-3 rounded-md hover:bg-muted transition-colors text-sm font-medium"
          >
            <item.icon className="h-5 w-5" />
            <span>{item.name}</span>
          </Link>
        ))}
      </nav>
    </div>
  );
}
