// src/components/Header.tsx

import React, { type FC } from "react";
import { Menu, LogOut, Loader2 } from "lucide-react"; // Menambahkan LogOut & Loader2
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { Sidebar } from "../Sidebar";

// Definisi Interface Props
interface NavProps {
  // Gunakan tipe yang lebih spesifik jika Anda tahu struktur datanya
  // Sementara ini menggunakan 'any' sesuai permintaan Anda, tapi sebaiknya diganti.
  userData: any;
  handleLogoutClick: () => void;
  isLoggingOut: boolean;
}

// Perbaikan Sintaks Komponen Fungsional
export function Header({
  userData,
  handleLogoutClick,
  isLoggingOut,
}: NavProps) {
  // Tentukan nama pengguna yang akan ditampilkan
  const username = userData?.user?.username || userData?.user?.name || "User";
  const levelStatus = userData?.user?.level_status;

  return (
    <header className="sticky top-0 z-10 border-b bg-background shadow-md">
      <div className="flex items-center justify-between h-16 px-4 lg:px-6">
        {/* Tombol Toggle Sidebar (Hanya di Mobile/Layar Kecil) */}
        <div className="lg:hidden">
          <Sheet>
            <SheetTrigger asChild>
              {/* Tombol menu menggunakan warna primary baru saat hover/focus */}
              <Button variant="ghost" size="icon">
                <Menu className="h-6 w-6" />
                <span className="sr-only">Toggle Sidebar</span>
              </Button>
            </SheetTrigger>

            {/* Konten Sheet: Sidebar Mobile */}
            <SheetContent side="left" className="p-0 w-64">
              {/* Sidebar Mobile */}
              <Sidebar className="border-r-0" />
            </SheetContent>
          </Sheet>
        </div>

        {/* Judul/Logo (Terlihat di Mobile) - Di Desktop, Sidebar sudah menampilkannya */}
        <div className="text-xl font-semibold lg:hidden text-primary">
          ANDIARTA
        </div>

        {/* Konten Header Kanan */}
        <div className="flex items-center space-x-4 ml-auto">
          {/* Info Pengguna */}
          <div className="mr-4 text-right hidden sm:block">
            <p className="text-sm font-medium text-foreground">{username}</p>

            {levelStatus && (
              // Menggunakan warna Primary (Hijau Tua) untuk badge
              <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-primary text-primary-foreground">
                {levelStatus}
              </span>
            )}
          </div>

          {/* Tombol Logout */}
          <Button
            variant="destructive"
            onClick={handleLogoutClick}
            disabled={isLoggingOut}
            className="h-10 px-4 py-2 text-sm font-medium text-gray-900 " // Beri sedikit padding agar tidak terlalu kecil
          >
            {isLoggingOut ? (
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            ) : (
              <LogOut className="mr-2 h-4 w-4" />
            )}
            Logout
          </Button>
        </div>
      </div>
    </header>
  );
}
