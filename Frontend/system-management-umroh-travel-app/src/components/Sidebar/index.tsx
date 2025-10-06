import { cn } from "@/lib/utils";
import { Home, User, UserPlus, Wallet } from "lucide-react";
import { Link } from "react-router-dom";
// Ganti dengan state atau hook yang sesuai dari router Anda untuk menentukan path aktif
const activePath = "/";

const navItems = [
  { name: "Home", icon: Home, path: "/dashboard" },
  { name: "Registrasi", icon: UserPlus, path: "/registrasi" },
  { name: "Profile", icon: User, path: "/profile" },
  { name: "Wallet", icon: Wallet, path: "/wallet" },
];

interface SidebarProps {
  className?: string;
}

export function Sidebar({ className }: SidebarProps) {
  return (
    <div
      className={cn(
        "flex flex-col border-r h-full bg-background p-4",
        className
      )}
    >
      {/* --- LOGO GAMBAR --- */}
      {/* Logo dari path public/images/logo/logo-andiarta-wisata.png */}
      <div className="mb-8  px-2">
        <img
          // Pastikan path ini benar sesuai struktur folder Anda di 'public'
          src="/images/logo/logo-andiarta-wisata.png"
          alt="ANDIARTA Tour & Travel Logo"
          // Mengatur lebar agar maksimum 48 unit dan responsif
          className="h-auto w-full max-w-[8rem]"
          style={{ filter: "drop-shadow(0 2px 4px rgba(0,0,0,0.1))" }}
        />
      </div>
      {/* -------------------- */}

      {/* Menu Navigasi */}
      <nav className="flex flex-col space-y-2">
        {navItems.map((item) => {
          const isActive = item.path === activePath;

          return (
            <Link
              key={item.name}
              to={item.path}
              // Menerapkan warna tema Hijau-Emas
              className={cn(
                "flex items-center space-x-3 p-3 rounded-lg transition-all text-sm font-medium",
                isActive
                  ? "bg-primary text-primary-foreground shadow-md"
                  : "text-foreground hover:bg-primary/10 hover:text-primary"
              )}
            >
              <item.icon className="h-5 w-5" />
              <span>{item.name}</span>
            </Link>
          );
        })}
      </nav>
    </div>
  );
}
