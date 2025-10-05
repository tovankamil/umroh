// src/components/Header.tsx (Pembaruan untuk Sidebar Mobile)

import React from "react";
import { Menu } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { Sidebar } from "../Sidebar"; // Impor Sidebar

export function Header() {
  return (
    <header className="sticky top-0 z-10 border-b bg-background shadow-sm">
      <div className="flex items-center justify-between h-16 px-4 lg:px-6">
        {/* Tombol Toggle Sidebar (Hanya di Mobile/Layar Kecil) */}
        {/* Tambahkan div ini agar tombol menu berada di kiri */}
        <div className="lg:hidden">
          <Sheet>
            <SheetTrigger asChild>
              <Button variant="ghost" size="icon">
                <Menu className="h-6 w-6" />
                <span className="sr-only">Toggle Sidebar</span>
              </Button>
            </SheetTrigger>

            {/* Konten Sheet: Sidebar Mobile */}
            {/* Lebar w-64 pada sheet dan padding 0 agar sidebar penuh di sheet */}
            <SheetContent side="left" className="p-0 w-64">
              {/* Panggil Sidebar tanpa class styling responsif.
                  Sidebar ini akan mengambil lebar penuh dari SheetContent.
              */}
              <Sidebar className="border-r-0" />
            </SheetContent>
          </Sheet>
        </div>

        {/* Judul/Logo (Terlihat di Mobile dan Desktop) */}
        <div className="text-xl font-semibold">Dashboard App</div>

        {/* Konten Header Kanan */}
        <div className="flex items-center space-x-4 ml-auto">
          {/* ... User Profile/Notifikasi */}
          <p className="text-sm hidden sm:block">Welcome, User!</p>
        </div>
      </div>
    </header>
  );
}
